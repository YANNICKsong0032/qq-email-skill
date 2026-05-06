#!/usr/bin/env python3
"""
配置验证 & 连接测试
用法: python3 setup.py

检查项：
  - config.json 是否存在且格式正确
  - 必填字段是否完整
  - IMAP 连接是否成功
  - SMTP 连接是否成功
  - 收件箱是否可读
"""

import json
import sys
from pathlib import Path

# 将 scripts 目录加入 path
sys.path.insert(0, str(Path(__file__).parent))
from utils import find_config, load_config, imap_connect, smtp_connect


def check_mark(ok, msg):
    icon = "✅" if ok else "❌"
    print(f"  {icon} {msg}")
    return ok


def main():
    print("🔍 QQ 邮箱 Skill 配置检查\n")
    all_ok = True

    # 1. 配置文件
    print("📁 配置文件")
    config_path = find_config()
    if not config_path:
        all_ok = False
        check_mark(False, "找不到配置文件")
        print("\n  修复：cp config.example.json config.json 并填写信息\n")
        sys.exit(1)
    check_mark(True, f"找到配置: {config_path}")

    # 2. 配置内容
    print("\n📋 配置内容")
    try:
        with open(config_path) as f:
            cfg = json.load(f)
        check_mark(True, "JSON 格式正确")
    except json.JSONDecodeError as e:
        all_ok = False
        check_mark(False, f"JSON 格式错误: {e}")
        sys.exit(1)

    required = {"email": "QQ邮箱地址", "password": "授权码"}
    for key, desc in required.items():
        val = cfg.get(key, "")
        if not val or "你的" in val or "xxx" in val.lower():
            all_ok = False
            check_mark(False, f"{desc} 未填写")
        else:
            masked = val[:3] + "***" if len(val) > 6 else "***"
            check_mark(True, f"{desc}: {masked}")

    optional = {
        "smtp_server": ("SMTP 服务器", "smtp.qq.com"),
        "smtp_port": ("SMTP 端口", 465),
        "name": ("发件人名称", "AI助手"),
        "max_fetch": ("每次最大读取数", 10),
    }
    for key, (desc, default) in optional.items():
        val = cfg.get(key, default)
        check_mark(True, f"{desc}: {val} (默认)" if val == default else f"{desc}: {val}")

    # 3. IMAP 连接
    print("\n📬 IMAP 连接测试")
    try:
        mail = imap_connect(cfg)
        check_mark(True, "IMAP 登录成功")

        status, data = mail.select("INBOX", readonly=True)
        if status == "OK":
            total = int(data[0])
            check_mark(True, f"收件箱可读，共 {total} 封邮件")

            # 检查未读
            status, data = mail.search(None, "UNSEEN")
            if status == "OK":
                unread = len(data[0].split()) if data[0] else 0
                check_mark(True, f"未读邮件: {unread} 封")
        else:
            all_ok = False
            check_mark(False, "无法读取收件箱")

        mail.logout()
    except Exception as e:
        all_ok = False
        check_mark(False, f"IMAP 连接失败: {e}")

    # 4. SMTP 连接
    print("\n📤 SMTP 连接测试")
    try:
        server = smtp_connect(cfg)
        check_mark(True, "SMTP 登录成功")
        server.quit()
    except Exception as e:
        all_ok = False
        check_mark(False, f"SMTP 连接失败: {e}")

    # 5. 安全守则
    print("\n🔒 安全守则")
    security_path = Path(__file__).parent.parent / "references" / "security.md"
    if security_path.exists():
        check_mark(True, "security.md 存在")
    else:
        check_mark(False, "security.md 缺失（可选但推荐）")

    # 6. 结果
    print("\n" + "─" * 40)
    if all_ok:
        print("🎉 一切就绪！可以开始使用了。")
        print("\n快速测试:")
        print("  python3 scripts/read_emails.py")
    else:
        print("⚠️  有问题需要修复，请检查上面的 ❌ 项。")
        print("\n常见修复:")
        print("  1. 确保已在 QQ 邮箱开启 IMAP/SMTP 服务")
        print("  2. 使用授权码（不是 QQ 密码）")
        print("  3. 检查网络连接")


if __name__ == "__main__":
    main()
