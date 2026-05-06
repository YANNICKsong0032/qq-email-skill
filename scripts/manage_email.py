#!/usr/bin/env python3
"""
邮件管理：标记已读/未读、删除、移动
用法:
  python3 manage_email.py --action read --nums "1,2,3"
  python3 manage_email.py --action unread --nums "1,2,3"
  python3 manage_email.py --action delete --nums "1,2,3"
  python3 manage_email.py --action read-all  # 标记所有未读为已读
"""

import json
import sys
import argparse
from utils import load_config, imap_connect


def main():
    parser = argparse.ArgumentParser(description="邮件管理")
    parser.add_argument("--action", choices=["read", "unread", "delete", "read-all"], required=True)
    parser.add_argument("--nums", help="邮件编号，逗号分隔")
    args = parser.parse_args()

    cfg = load_config()

    if args.action != "read-all" and not args.nums:
        print(json.dumps({"error": "--nums 参数必须提供（read-all 除外）"}))
        sys.exit(1)

    try:
        mail = imap_connect(cfg)
    except Exception as e:
        print(json.dumps({"error": f"连接邮箱失败: {e}"}))
        sys.exit(1)

    try:
        mail.select("INBOX")

        if args.action == "read-all":
            status, data = mail.search(None, "UNSEEN")
            if status != "OK" or not data[0]:
                print(json.dumps({"message": "没有未读邮件"}))
                return
            nums = data[0].split()
        else:
            nums = [n.strip().encode() for n in args.nums.split(",")]

        results = []
        for num in nums:
            try:
                if args.action in ("read", "read-all"):
                    mail.store(num, "+FLAGS", "\\Seen")
                    results.append({"num": num.decode(), "status": "marked_read"})
                elif args.action == "unread":
                    mail.store(num, "-FLAGS", "\\Seen")
                    results.append({"num": num.decode(), "status": "marked_unread"})
                elif args.action == "delete":
                    mail.store(num, "+FLAGS", "\\Deleted")
                    results.append({"num": num.decode(), "status": "deleted"})
            except Exception as e:
                results.append({"num": num.decode(), "status": "error", "error": str(e)})

        if args.action == "delete":
            mail.expunge()

        print(json.dumps({
            "action": args.action,
            "count": len(results),
            "results": results,
        }, ensure_ascii=False, indent=2))

    finally:
        try:
            mail.logout()
        except Exception:
            pass


if __name__ == "__main__":
    main()
