<div align="center">

<img src="https://img.shields.io/badge/📬-QQ_Email_Skill-0A0A0A?style=for-the-badge&labelColor=1a1a2e&color=16213e" alt="QQ Email Skill" />

# 📬 QQ Email Skill

### Email Superpowers for AI Agents

*Read · Analyze · Reply · Manage — all via IMAP/SMTP*

<br>

[![MIT License](https://img.shields.io/badge/License-MIT-2ecc71?style=flat-square)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Zero Deps](https://img.shields.io/badge/Dependencies-Zero-f39c12?style=flat-square)](#-dependencies)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-9b59b6?style=flat-square)](https://github.com/openclaw/openclaw)

<br>

**[Quick Start](#-quick-start)** · **[Features](#-features)** · **[Usage](#-usage)** · **[Security](#-security)**

</div>

---

## ✨ Features

```
📥 READ & SEARCH                     📤 REPLY & SEND
──────────────────                   ──────────────────
▸ Smart inbox filter                 ▸ SMTP with threading
  sender / subject / date            ▸ Duplicate check
▸ Native IMAP search                   no double replies
  fast even on large boxes           ▸ Force mode available
▸ HTML auto → readable text

📊 ANALYTICS                         🔒 SECURITY
──────────────────                   ──────────────────
▸ Inbox stats                        ▸ Customizable filters
  top senders / hot topics           ▸ No sensitive info leaks
▸ Batch mark read/unread             ▸ Zero dependencies
▸ 3× auto retry                        pure Python stdlib
```

---

## 🚀 Quick Start

> **3 steps. 2 minutes.**

**1** — Get authorization code: *QQ Mail → Settings → Account → IMAP → Generate*

**2** — Install
```bash
git clone https://github.com/YANNICKsong0032/qq-email-skill.git && cd qq-email-skill
cp config.example.json config.json   # ← fill in your credentials
```

**3** — Verify
```bash
python3 scripts/setup.py
```

```
🔍 QQ Email Skill — Configuration Check

📁 Config File        ✅ config.json
📋 Contents           ✅ QQ: 123***  |  Auth: abc***
📬 IMAP Connection    ✅ 42 emails, 3 unread
📤 SMTP Connection    ✅ Login OK
🔒 Security Rules     ✅ security.md

🎉 All set!
```

---

## 📖 Usage

### 📥 Read Emails

```bash
read_emails.py                              # Latest unread
read_emails.py --from "boss@co.com"         # By sender
read_emails.py --subject "meeting"          # By subject
read_emails.py --days 3                     # Last 3 days
read_emails.py --all --raw                  # All + full body
read_emails.py --from "x" --days 7 --limit 20   # Combined
```

### 📤 Reply

```bash
reply_email.py \
  --to "sender@example.com" \
  --subject "Re: Topic" \
  --body "Got it, thanks!" \
  --in-reply-to "<original-id>"
```

### 📊 Stats

```bash
python3 scripts/stats.py
```

```
📬 Mailbox — 3762600312@qq.com

📬 Total: 156  |  📨 Unread: 8

👤 Top Senders            📌 Hot Topics
   GitHub — 45               "Pull Request" — 12×
   boss — 23                 "会议通知" — 8×
```

---

## 📁 Structure

```
qq-email-skill/
├── SKILL.md                    # Entry point
├── config.example.json         # Template
├── config.json                 # Yours (git-ignored)
├── security.md                 # 🔒 Rules
├── replied.json                # Reply log (auto)
├── scripts/
│   ├── read_emails.py          # 📥 Read
│   ├── reply_email.py          # 📤 Reply
│   ├── stats.py                # 📊 Stats
│   ├── setup.py                # ⚙️ Checker
│   └── mark_as_read.py         # ✅ Mark read
└── references/
    └── qq-email-auth.md        # 🔑 Auth guide
```

---

## ⚙️ Config

```json
{
  "email": "your@qq.com",
  "auth_code": "your-code",
  "imap_server": "imap.qq.com",
  "smtp_server": "smtp.qq.com",
  "max_retries": 3,
  "retry_delay": 2
}
```

| Key | Default | Description |
|-----|---------|-------------|
| `email` | — | QQ email address |
| `auth_code` | — | IMAP/SMTP auth code |
| `imap_server` | `imap.qq.com` | IMAP host |
| `smtp_server` | `smtp.qq.com` | SMTP host |
| `max_retries` | `3` | Retry attempts |
| `retry_delay` | `2` | Seconds between retries |

---

## 🔒 Security

| | Rule |
|---|------|
| 🚫 | Never log auth codes or passwords |
| 🔐 | Filter sensitive info before output |
| ✋ | User confirmation before sending |
| 🚫 | No auto-forwarding to unknowns |

→ Full rules: [`security.md`](security.md)

---

## 📦 Dependencies

> **None.** Pure Python standard library.

`imaplib` · `smtplib` · `email` · `json` · `argparse`

---

## 🤝 Contributing

```
Fork → Branch → Commit → Push → PR
```

---

## 📄 License

[MIT](LICENSE) — use freely.

<br>

<div align="center">

**Made with ❤️ for [OpenClaw](https://github.com/openclaw/openclaw)**

*If this saved you time, a ⭐ goes a long way!*

</div>
