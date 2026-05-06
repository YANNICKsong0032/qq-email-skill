#!/usr/bin/env python3
"""
收件箱统计摘要
用法: python3 stats.py [--days 7] [--top 10]

输出：
  - 总邮件数 / 未读数
  - 最近 N 天的邮件数量（使用 IMAP 原生搜索，高效）
  - Top 发件人排行
  - 邮件主题关键词统计
"""

import json
import sys
import argparse
from collections import Counter
from typing import Any

from utils import load_config, imap_connect, imap_date_search, decode_str


def main():
    parser = argparse.ArgumentParser(description="收件箱统计")
    parser.add_argument("--days", type=int, default=7, help="统计最近N天（默认7）")
    parser.add_argument("--top", type=int, default=10, help="Top N 排行（默认10）")
    args = parser.parse_args()

    cfg = load_config()

    try:
        mail = imap_connect(cfg)
    except Exception as e:
        print(json.dumps({"error": f"连接失败: {e}"}))
        sys.exit(1)

    try:
        mail.select("INBOX", readonly=True)

        # 总数
        status, data = mail.search(None, "ALL")
        all_nums = data[0].split() if status == "OK" and data[0] else []
        total = len(all_nums)

        # 未读
        status, data = mail.search(None, "UNSEEN")
        unread_nums = data[0].split() if status == "OK" and data[0] else []
        unread = len(unread_nums)

        # 最近 N 天 — 用 IMAP 原生搜索，不用全量 fetch
        recent_nums = imap_date_search(mail, args.days)
        recent_count = len(recent_nums)

        # 分析发件人和主题（只取最近 N 天的邮件头，最多 100 封）
        sample = recent_nums[-100:] if len(recent_nums) > 100 else recent_nums
        senders: Counter = Counter()
        subjects: Counter = Counter()

        for num in sample:
            status, msg_data = mail.fetch(num, "(RFC822.HEADER)")
            if status != "OK":
                continue
            from email import message_from_bytes
            msg = message_from_bytes(msg_data[0][1])

            from_addr = msg.get("From", "")
            if "<" in from_addr and ">" in from_addr:
                name = from_addr.split("<")[0].strip().strip('"')
                addr = from_addr.split("<")[1].split(">")[0]
            else:
                name = from_addr
                addr = from_addr
            if addr != cfg["email"]:
                senders[name or addr] += 1

            subject = decode_str(msg.get("Subject", ""))
            if subject:
                subjects[subject[:30]] += 1

        result = {
            "inbox_total": total,
            "unread": unread,
            f"last_{args.days}_days": recent_count,
            "top_senders": senders.most_common(args.top),
            "top_subjects": subjects.most_common(args.top),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    finally:
        try:
            mail.logout()
        except Exception:
            pass


if __name__ == "__main__":
    main()
