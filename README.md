<div align="center">

# 📬 QQ Email Skill

**Email superpowers for AI Agents**

*Read · Analyze · Reply · Manage — all via IMAP/SMTP*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange.svg)](#-dependencies)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://github.com/openclaw/openclaw)

[Quick Start](#-quick-start) · [Features](#-features) · [Usage](#-usage) · [Security](#-security) · [Contributing](#-contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📥 Read & Search
- **Smart inbox** — unread, filtered by sender / subject / date
- **Native IMAP search** — date filters without full fetch
- **HTML → Text** — auto-converts HTML emails to readable text

</td>
<td width="50%">

### 📤 Reply & Send
- **SMTP sending** with in-reply-to threading
- **Duplicate check** — logs to `replied.json`, no double replies
- **Force mode** — `--force` to skip duplicate check

</td>
</tr>
<tr>
<td>

### 📊 Analytics & Management
- **Inbox stats** — top senders, hot topics, unread count
- **Batch operations** — mark read / unread, delete
- **3x auto retry** — network hiccups handled gracefully

</td>
<td>

### 🔒 Security First
- **Customizable filters** — prevent sensitive info leaks
- **Zero dependencies** — pure Python standard library
- **Auth code only** — no passwords stored

</td>
</tr>
</table>

---

## 🚀 Quick Start

### 1. Get an Authorization Code

> **QQ Mail** → Settings → Account → POP3/IMAP/SMTP → Enable IMAP → Generate code

### 2. Install & Configure

```bash
git clone https://github.com/YANNICKsong0032/qq-email-skill.git
cd qq-email-skill
cp config.example.json config.json
# Edit config.json with your credentials
```

### 3. Verify Setup

```bash
python3 scripts/setup.py
```

```
🔍 QQ Email Skill — Configuration Check

📁 Config File        ✅ config.json
📋 Contents           ✅ QQ Email: 123***  |  Auth Code: abc***
📬 IMAP Connection    ✅ Login OK — 42 emails, 3 unread
📤 SMTP Connection    ✅ Login OK
🔒 Security Rules     ✅ security.md exists

🎉 All set!
```

---

## 📖 Usage

### 📥 Read Emails

```bash
# Latest unread (default)
python3 scripts/read_emails.py

# Filter by sender
python3 scripts/read_emails.py --from "boss@company.com"

# Filter by subject keyword
python3 scripts/read_emails.py --subject "meeting"

# Last 3 days (fast — native IMAP search)
python3 scripts/read_emails.py --days 3

# Include read + full body
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

### 📊 Inbox Summary

```bash
python3 scripts/stats.py
```

```
📬 Mailbox Stats — 3762600312@qq.com

📬 Total: 156  |  📨 Unread: 8

👤 Top Senders:
   1. GitHub <noreply@github.com> — 45
   2. boss@company.com — 23

📌 Hot Topics:
   1. "Pull Request" — 12×
   2. "会议通知" — 8×
```

---

## 📁 Project Structure

```
qq-email-skill/
├── SKILL.md                    # Skill definition (entry)
├── config.example.json         # Config template
├── config.json                 # Your config (git-ignored)
├── security.md                 # 🔒 Security rules
├── replied.json                # Reply log (auto-created)
├── scripts/
│   ├── read_emails.py          # 📥 Read & filter
│   ├── reply_email.py          # 📤 Reply & send
│   ├── stats.py                # 📊 Statistics
│   ├── setup.py                # ⚙️ Config checker
│   └── mark_as_read.py         # ✅ Mark as read
└── references/
    └── qq-email-auth.md        # 🔑 Auth code guide
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
| `imap_server` | `imap.qq.com` | IMAP server |
| `smtp_server` | `smtp.qq.com` | SMTP server |
| `max_retries` | `3` | Max retry attempts |
| `retry_delay` | `2` | Seconds between retries |

---

## 🔒 Security

> **Full rules:** [`security.md`](security.md)

- 🚫 **Never log** auth codes or passwords
- 🔐 **Filter sensitive info** before output (phone, address, etc.)
- ✋ **User confirmation** required before sending
- 🚫 **No auto-forwarding** to unknown addresses

---

## 📦 Dependencies

**Zero.** Pure Python standard library:

`imaplib` · `smtplib` · `email` · `json` · `argparse`

---

## 🤝 Contributing

1. **Fork** this repository
2. **Create** a feature branch — `git checkout -b feature/amazing`
3. **Commit** your changes — `git commit -m 'Add amazing feature'`
4. **Push** to the branch — `git push origin feature/amazing`
5. **Open** a Pull Request

---

## 📄 License

[MIT License](LICENSE) — free to use, modify, and distribute.

---

<div align="center">

**Built with ❤️ for the [OpenClaw](https://github.com/openclaw/openclaw) ecosystem**

⭐ Star this repo if you find it useful!

</div>
