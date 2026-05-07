# 📬 QQ Email Skill

> Email superpowers for AI Agents — **read, analyze, reply, and manage** QQ Mail via IMAP/SMTP

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-green.svg)](https://www.python.org/)
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-orange.svg)](#dependencies)

---

## ✨ Features

- 📥 **Smart Inbox** — Read unread emails, filter by sender / subject / date
- 📤 **Auto Reply** — SMTP sending with duplicate check to avoid double replies
- 📊 **Statistics** — Inbox overview, top senders, hot topics
- 🗂️ **Mail Management** — Mark read / unread, batch operations, delete
- 🔒 **Security Rules** — Customizable info filters to prevent data leaks
- 🔄 **Auto Retry** — Network hiccups? 3 retries have your back
- 🧹 **HTML → Text** — HTML emails auto-converted to readable plain text
- ⚡ **Native IMAP Search** — Date filters without fetching everything; fast even for large inboxes
- 🛡️ **Zero Dependencies** — Pure standard library, no `pip install` needed

---

## 🚀 Quick Start

### 1. Get an Authorization Code

> QQ Mail → Settings → Account → POP3/IMAP/SMTP → Enable IMAP → Generate authorization code

### 2. Install

```bash
git clone https://github.com/YANNICKsong0032/qq-email-skill.git
cd qq-email-skill
cp config.example.json config.json
# Edit config.json with your QQ email and authorization code
```

### 3. Verify

```bash
python3 scripts/setup.py
```

```
🔍 QQ Email Skill — Configuration Check

📁 Config File
  ✅ Found: config.json
📋 Config Contents
  ✅ QQ Email: 123***
  ✅ Auth Code: abc***
📬 IMAP Connection Test
  ✅ IMAP login succeeded
  ✅ Inbox readable — 42 emails total
  ✅ Unread: 3
📤 SMTP Connection Test
  ✅ SMTP login succeeded
🔒 Security Rules
  ✅ security.md exists

🎉 All set!
```

---

## 📖 Usage

### 📥 Read Emails

```bash
# Read latest unread (default)
python3 scripts/read_emails.py

# Filter by sender
python3 scripts/read_emails.py --from "boss@company.com"

# Filter by subject keyword
python3 scripts/read_emails.py --subject "meeting"

# Last 3 days (efficient — native IMAP search)
python3 scripts/read_emails.py --days 3

# Include read emails + full body
python3 scripts/read_emails.py --all --raw

# Combine filters
python3 scripts/read_emails.py --from "client@xx.com" --days 7 --limit 20
```

### 📤 Reply to Emails

```bash
python3 scripts/reply_email.py \
  --to "sender@example.com" \
  --subject "Re: Original Subject" \
  --body "Got it, I'll take a look." \
  --in-reply-to "<original-Message-ID>"
```

- ✅ Logged to `replied.json` — no duplicate replies
- 🔧 Use `--force` to skip the duplicate check

### 📊 Inbox Summary

```bash
python3 scripts/stats.py
```

```
📬 邮箱统计 — 3762600312@qq.com

📬 总邮件: 156 封
📨 未读邮件: 8 封

👤 Top 5 发件人:
  1. GitHub <noreply@github.com> — 45 封
  2. boss@company.com — 23 封
  ...

📌 热门主题:
  1. "Pull Request" — 12 次
  2. "会议通知" — 8 次
  ...
```

---

## 📁 File Structure

```
qq-email-skill/
├── SKILL.md                    # Skill definition (entry point)
├── README.md                   # This file
├── config.example.json         # Config template
├── config.json                 # Your config (git-ignored)
├── security.md                 # Security rules
├── replied.json                # Reply log (auto-created)
├── scripts/
│   ├── read_emails.py          # Read & filter emails
│   ├── reply_email.py          # Reply to emails
│   ├── stats.py                # Inbox statistics
│   ├── setup.py                # Configuration checker
│   └── mark_as_read.py         # Mark emails as read
└── references/
    └── qq-email-auth.md        # Auth code setup guide
```

---

## ⚙️ Configuration

`config.json`:

```json
{
  "email": "your@qq.com",
  "auth_code": "your-authorization-code",
  "imap_server": "imap.qq.com",
  "smtp_server": "smtp.qq.com",
  "max_retries": 3,
  "retry_delay": 2
}
```

| Field | Default | Description |
|-------|---------|-------------|
| `email` | — | Your QQ email address |
| `auth_code` | — | IMAP/SMTP authorization code |
| `imap_server` | `imap.qq.com` | IMAP server address |
| `smtp_server` | `smtp.qq.com` | SMTP server address |
| `max_retries` | `3` | Max retry attempts |
| `retry_delay` | `2` | Seconds between retries |

---

## 🔒 Security

See [`security.md`](security.md) for the full security rules. Key points:

- **Never log** authorization codes or passwords
- **Filter sensitive info** before output (phone numbers, addresses, etc.)
- **User confirmation** required before sending emails
- **No auto-forwarding** to unknown addresses

---

## 📦 Dependencies

**Zero.** Pure Python standard library:

- `imaplib` — IMAP connection
- `smtplib` — SMTP sending
- `email` — Email parsing
- `json` — Config & logs
- `argparse` — CLI parsing

---

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Built for the [OpenClaw](https://github.com/openclaw/openclaw) agent ecosystem
- Thanks to QQ Mail for providing IMAP/SMTP access
