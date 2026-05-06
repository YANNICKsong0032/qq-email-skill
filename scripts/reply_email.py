#!/usr/bin/env python3
"""
通过 QQ 邮箱 SMTP 发送邮件回复
用法:
  python3 reply_email.py --to "xxx@qq.com" --subject "Re: xxx" --body "回复内容"
  python3 reply_email.py --to "xxx@qq.com" --subject "Re: xxx" --body "回复内容" --in-reply-to "<message-id>"

回复追踪：
  自动记录到 replied.json，避免重复回复。
  使用 --force 跳过重复检查。
"""

import json
import sys
import argparse
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from utils import load_config, smtp_connect

REPLIED_PATH = Path(__file__).parent.parent / "replied.json"


def load_replied():
    if REPLIED_PATH.exists():
        with open(REPLIED_PATH) as f:
            return json.load(f)
    return {"replied_ids": []}


def save_replied(data):
    with open(REPLIED_PATH, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="回复邮件")
    parser.add_argument("--to", required=True, help="收件人地址")
    parser.add_argument("--subject", required=True, help="邮件主题")
    parser.add_argument("--body", required=True, help="回复内容")
    parser.add_argument("--in-reply-to", help="原邮件 Message-ID")
    parser.add_argument("--references", help="原邮件 References")
    parser.add_argument("--force", action="store_true", help="跳过重复检查")
    args = parser.parse_args()

    cfg = load_config()

    # 重复检查
    if args.in_reply_to and not args.force:
        replied = load_replied()
        if args.in_reply_to in replied["replied_ids"]:
            print(json.dumps({
                "status": "skipped",
                "reason": "该邮件已回复过",
                "message_id": args.in_reply_to,
                "hint": "使用 --force 强制发送"
            }))
            sys.exit(0)

    # 构建邮件
    msg = MIMEMultipart()
    # 中文名称需要 RFC2047 编码，邮箱地址不编码
    from_name = Header(cfg.get('name', 'AI助手'), 'utf-8').encode()
    msg["From"] = f"{from_name} <{cfg['email']}>"
    msg["To"] = args.to
    msg["Subject"] = Header(args.subject, "utf-8")

    if args.in_reply_to:
        msg["In-Reply-To"] = args.in_reply_to
        msg["References"] = args.references or args.in_reply_to

    msg.attach(MIMEText(args.body, "plain", "utf-8"))

    # 发送
    try:
        server = smtp_connect(cfg)
        server.sendmail(cfg["email"], [args.to], msg.as_string())
        server.quit()
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False))
        sys.exit(1)

    # 记录已回复
    if args.in_reply_to:
        replied = load_replied()
        replied["replied_ids"].append(args.in_reply_to)
        # 只保留最近 500 条
        replied["replied_ids"] = replied["replied_ids"][-500:]
        save_replied(replied)

    print(json.dumps({
        "status": "sent",
        "to": args.to,
        "subject": args.subject,
        "in_reply_to": args.in_reply_to,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
