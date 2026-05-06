#!/usr/bin/env python3
"""
读取QQ邮箱邮件
用法: python3 read_emails.py [数量限制]

高级用法:
  python3 read_emails.py                    # 默认读取最新未读
  python3 read_emails.py --limit 5          # 指定数量
  python3 read_emails.py --from "xxx@qq.com" # 按发件人过滤
  python3 read_emails.py --subject "会议"    # 按主题关键词过滤
  python3 read_emails.py --days 3           # 只看最近3天（用 IMAP 原生搜索）
  python3 read_emails.py --all              # 包含已读邮件
  python3 read_emails.py --raw              # 不截断正文
"""

import json
import sys
import argparse
from typing import Any

from utils import load_config, imap_connect, imap_date_search, parse_email_msg


def main():
    parser = argparse.ArgumentParser(description="读取QQ邮箱邮件")
    parser.add_argument("positional_limit", nargs="?", type=int, help="数量限制（位置参数）")
    parser.add_argument("--limit", type=int, help="数量限制")
    parser.add_argument("--from", dest="from_addr", help="按发件人过滤")
    parser.add_argument("--subject", help="按主题关键词过滤")
    parser.add_argument("--days", type=int, help="只看最近N天的邮件（高效，用 IMAP 原生搜索）")
    parser.add_argument("--all", action="store_true", help="包含已读邮件")
    parser.add_argument("--raw", action="store_true", help="不截断正文（完整输出）")
    args = parser.parse_args()

    cfg = load_config()
    limit = args.limit or args.positional_limit or cfg.get("max_fetch", 10)
    skip_keywords = cfg.get("skip_keywords", [])

    try:
        mail = imap_connect(cfg)
    except Exception as e:
        print(json.dumps({"error": f"连接邮箱失败: {e}", "fix": "检查网络和授权码是否正确"}))
        sys.exit(1)

    try:
        mail.select("INBOX", readonly=True)

        # 优先用 IMAP 原生搜索（高效）
        if args.days:
            msg_nums = imap_date_search(mail, args.days)
        else:
            search_criteria = "ALL" if args.all else "UNSEEN"
            status, data = mail.search(None, search_criteria)
            msg_nums = data[0].split() if status == "OK" and data[0] else []

        if not msg_nums:
            print(json.dumps({
                "emails": [],
                "total_unread": 0,
                "message": "没有未读邮件" if not args.all else "收件箱为空"
            }))
            return

        # 从最新的开始取
        emails = []
        body_max = 999999 if args.raw else 3000

        for num in reversed(msg_nums):
            if len(emails) >= limit:
                break

            status, msg_data = mail.fetch(num, "(RFC822)")
            if status != "OK":
                continue

            from email import message_from_bytes
            msg = message_from_bytes(msg_data[0][1])
            parsed = parse_email_msg(
                msg, num=num,
                skip_keywords=skip_keywords,
                own_email=cfg["email"],
                max_body_len=body_max,
            )
            if not parsed:
                continue

            # 应用过滤条件
            if args.from_addr and args.from_addr.lower() not in parsed["from_addr"].lower():
                continue
            if args.subject and args.subject.lower() not in parsed["subject"].lower():
                continue

            emails.append(parsed)

        result = {
            "total_inbox": len(msg_nums),
            "emails_returned": len(emails),
            "filters": {
                "from": args.from_addr,
                "subject": args.subject,
                "days": args.days,
                "include_read": args.all,
            },
            "emails": emails,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    finally:
        try:
            mail.logout()
        except Exception:
            pass


if __name__ == "__main__":
    main()
