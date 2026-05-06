#!/usr/bin/env python3
"""
QQ 邮箱工具库 — 共享函数
"""

import json
import os
import sys
import imaplib
import smtplib
import time
import re
from pathlib import Path
from email.header import decode_header
from email.utils import parseaddr
from html.parser import HTMLParser
from typing import Optional, Dict, List, Any, Callable, TypeVar

T = TypeVar("T")


# ─── 重试 ───────────────────────────────────────────

def with_retry(fn: Callable[..., T], max_retries: int = 3, delay: float = 2.0) -> Callable[..., T]:
    """重试包装器。用法: with_retry(connect_fn)() 而不是 retry(fn)()()"""
    def wrapper(*args, **kwargs) -> T:
        last_exc = None
        for attempt in range(max_retries):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                last_exc = e
                if attempt < max_retries - 1:
                    time.sleep(delay * (attempt + 1))
        raise last_exc
    return wrapper


# ─── 配置 ───────────────────────────────────────────

def find_config() -> Optional[Path]:
    """按优先级查找配置文件"""
    env_path = os.environ.get("QQ_EMAIL_CONFIG")
    if env_path and Path(env_path).exists():
        return Path(env_path)
    skill_config = Path(__file__).parent.parent / "config.json"
    if skill_config.exists():
        return skill_config
    legacy = Path.home() / ".openclaw" / "email-config.json"
    if legacy.exists():
        return legacy
    return None


def load_config() -> Dict[str, Any]:
    """加载配置，失败时给出友好提示"""
    config_path = find_config()
    if not config_path:
        print(json.dumps({
            "error": "找不到配置文件",
            "fix": "复制 config.example.json 为 config.json 并填写你的 QQ 邮箱信息"
        }))
        sys.exit(1)
    try:
        with open(config_path) as f:
            cfg = json.load(f)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"配置文件 JSON 格式错误: {e}"}))
        sys.exit(1)

    missing = []
    for key in ("email", "password"):
        if not cfg.get(key) or cfg[key].startswith("你的"):
            missing.append(key)
    if missing:
        print(json.dumps({
            "error": f"配置文件缺少必要字段: {', '.join(missing)}",
            "fix": "编辑 config.json 填写真实的 QQ 邮箱和授权码"
        }))
        sys.exit(1)

    cfg.setdefault("smtp_server", "smtp.qq.com")
    cfg.setdefault("smtp_port", 465)
    cfg.setdefault("name", "AI助手")
    cfg.setdefault("max_fetch", 10)
    cfg.setdefault("skip_keywords", [
        "noreply", "no-reply", "no_reply", "donotreply",
        "mailer-daemon", "postmaster", "notifications",
        "newsletter", "marketing", "alert",
    ])
    return cfg


# ─── 邮箱连接 ───────────────────────────────────────

def imap_connect(cfg: Dict[str, Any], timeout: int = 30) -> imaplib.IMAP4_SSL:
    """连接 IMAP 并返回 mail 对象（带重试）"""
    def _connect() -> imaplib.IMAP4_SSL:
        mail = imaplib.IMAP4_SSL("imap.qq.com", timeout=timeout)
        mail.login(cfg["email"], cfg["password"])
        return mail
    return with_retry(_connect)()


def smtp_connect(cfg: Dict[str, Any]) -> smtplib.SMTP_SSL:
    """连接 SMTP 并返回 server 对象（带重试）"""
    def _connect() -> smtplib.SMTP_SSL:
        server = smtplib.SMTP_SSL(cfg["smtp_server"], cfg["smtp_port"], timeout=30)
        server.login(cfg["email"], cfg["password"])
        return server
    return with_retry(_connect)()


# ─── 解码 ───────────────────────────────────────────

def decode_str(s: Optional[str]) -> str:
    """解码 MIME 编码的字符串"""
    if s is None:
        return ""
    decoded_parts = decode_header(s)
    result = ""
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            result += part.decode(charset or "utf-8", errors="replace")
        else:
            result += part
    return result


class HTMLToTextParser(HTMLParser):
    """HTML → 纯文本，保留换行结构"""

    BLOCK_TAGS = {"br", "p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
                  "li", "tr", "blockquote", "hr", "pre", "section", "article"}
    SKIP_TAGS = {"script", "style", "head"}

    def __init__(self):
        super().__init__()
        self.parts: List[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list):
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
        if tag in self.BLOCK_TAGS and self._skip_depth == 0:
            if tag == "br":
                self.parts.append("\n")
            elif tag in ("p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
                         "li", "tr", "blockquote", "section", "article"):
                self.parts.append("\n")
            elif tag == "hr":
                self.parts.append("\n---\n")

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
        if tag in ("p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote"):
            if self._skip_depth == 0:
                self.parts.append("\n")

    def handle_data(self, data: str):
        if self._skip_depth == 0:
            self.parts.append(data)

    def get_text(self) -> str:
        raw = "".join(self.parts)
        # 合并连续空行为单个换行
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()


def html_to_text(html: str) -> str:
    """将 HTML 转为纯文本，保留结构"""
    parser = HTMLToTextParser()
    try:
        parser.feed(html)
        return parser.get_text()
    except Exception:
        return html


def get_email_body(msg: Any, max_len: int = 3000) -> str:
    """提取邮件正文，优先纯文本，其次从 HTML 转换"""
    body = ""
    html_body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in disposition:
                continue
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                body += payload.decode(charset, errors="replace")
            elif content_type == "text/html":
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                html_body += payload.decode(charset, errors="replace")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            content_type = msg.get_content_type()
            if content_type == "text/html":
                html_body = payload.decode(charset, errors="replace")
            else:
                body = payload.decode(charset, errors="replace")

    if body:
        return body[:max_len]
    if html_body:
        return html_to_text(html_body)[:max_len]
    return ""


def get_attachments(msg: Any) -> List[Dict[str, Any]]:
    """提取附件信息"""
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in disposition:
                filename = decode_str(part.get_filename())
                size = len(part.get_payload(decode=True) or b"")
                attachments.append({"filename": filename, "size_bytes": size})
    return attachments


def is_auto_mail(from_addr: str, skip_keywords: List[str]) -> bool:
    """判断是否为自动邮件"""
    lower = from_addr.lower()
    return any(kw in lower for kw in skip_keywords)


def parse_email_msg(msg: Any, num: Optional[int] = None,
                    skip_keywords: Optional[List[str]] = None,
                    own_email: Optional[str] = None,
                    max_body_len: int = 3000) -> Optional[Dict[str, Any]]:
    """解析 email.message.Message 为 dict"""
    from_name, from_addr = parseaddr(msg.get("From", ""))

    if own_email and from_addr == own_email:
        return None
    if skip_keywords and is_auto_mail(from_addr, skip_keywords):
        return None

    result: Dict[str, Any] = {
        "id": msg.get("Message-ID", "").strip(),
        "from_name": decode_str(from_name),
        "from_addr": from_addr,
        "to": msg.get("To", ""),
        "subject": decode_str(msg.get("Subject", "")),
        "date": msg.get("Date", ""),
        "body": get_email_body(msg, max_len=max_body_len),
        "attachments": get_attachments(msg),
    }
    if num is not None:
        result["num"] = str(num)
    return result


# ─── IMAP 搜索工具 ───────────────────────────────────

def imap_date_search(mail: imaplib.IMAP4_SSL, days: int) -> List[bytes]:
    """用 IMAP 原生搜索获取最近 N 天的邮件编号（比全量 fetch 高效得多）"""
    from datetime import datetime, timedelta
    date_str = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
    status, data = mail.search(None, f'(SINCE "{date_str}")')
    if status == "OK" and data[0]:
        return data[0].split()
    return []
