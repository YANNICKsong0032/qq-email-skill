# 📬 QQ 邮箱 Skill

> 为 AI Agent 提供 QQ 邮箱的**读取、分析、回复、管理**能力

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-green.svg)](https://www.python.org/)
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-orange.svg)](#依赖)

---

## ✨ 特性

- 📥 **智能读取** — 未读邮件、按发件人/主题/日期过滤
- 📤 **自动回复** — SMTP 发送，含重复检查，避免二次回复
- 📊 **统计摘要** — 收件箱概况、Top 发件人、热门主题
- 🗂️ **邮件管理** — 标记已读/未读、批量操作、删除
- 🔒 **安全守则** — 可自定义的信息过滤规则，防泄露
- 🔄 **自动重试** — 网络抖动不怕，3 次重试兜底
- 🧹 **HTML 转文本** — HTML 邮件自动转可读纯文本
- ⚡ **IMAP 原生搜索** — 日期过滤不拉全量，大邮箱也秒出
- 🛡️ **零依赖** — 纯标准库，`pip install` 不需要

## 🚀 快速开始

### 1. 获取授权码

> QQ 邮箱 → 设置 → 账户 → POP3/IMAP/SMTP 服务 → 开启 IMAP → 生成授权码

### 2. 安装

```bash
git clone https://github.com/YANNICKsong0032/qq-email-skill.git
cd qq-email-skill
cp config.example.json config.json
# 编辑 config.json，填写你的 QQ 邮箱和授权码
```

### 3. 验证

```bash
python3 scripts/setup.py
```

```
🔍 QQ 邮箱 Skill 配置检查

📁 配置文件
  ✅ 找到配置: config.json
📋 配置内容
  ✅ QQ邮箱地址: 123***
  ✅ 授权码: abc***
📬 IMAP 连接测试
  ✅ IMAP 登录成功
  ✅ 收件箱可读，共 42 封邮件
  ✅ 未读邮件: 3 封
📤 SMTP 连接测试
  ✅ SMTP 登录成功
🔒 安全守则
  ✅ security.md 存在

🎉 一切就绪！
```

## 📖 使用方法

### 📥 读取邮件

```bash
# 默认读取最新未读
python3 scripts/read_emails.py

# 按发件人过滤
python3 scripts/read_emails.py --from "boss@company.com"

# 按主题关键词
python3 scripts/read_emails.py --subject "会议"

# 最近 3 天（高效，IMAP 原生搜索）
python3 scripts/read_emails.py --days 3

# 包含已读 + 不截断正文
python3 scripts/read_emails.py --all --raw

# 组合使用
python3 scripts/read_emails.py --from "client@xx.com" --days 7 --limit 20
```

### 📤 回复邮件

```bash
python3 scripts/reply_email.py \
  --to "sender@example.com" \
  --subject "Re: 原主题" \
  --body "收到，我看看~" \
  --in-reply-to "<原邮件Message-ID>"
```

- ✅ 自动记录到 `replied.json`，不会重复回复
- 🔧 用 `--force` 跳过重复检查

### 📊 收件箱统计

```bash
python3 scripts/stats.py              # 最近 7 天
python3 scripts/stats.py --days 30    # 最近 30 天
python3 scripts/stats.py --top 5      # Top 5
```

```json
{
  "inbox_total": 42,
  "unread": 3,
  "last_7_days": 15,
  "top_senders": [["老板", 8], ["GitHub", 5], ["Steam", 3]],
  "top_subjects": [["周报", 4], ["PR Review", 3]]
}
```

### 🗂️ 管理邮件

```bash
python3 scripts/manage_email.py --action read --nums "1,2,3"    # 标记已读
python3 scripts/manage_email.py --action unread --nums "1"      # 标记未读
python3 scripts/manage_email.py --action read-all               # 全部已读
python3 scripts/manage_email.py --action delete --nums "5,6"    # 删除
```

## ⚙️ 配置

### 配置文件查找顺序

| 优先级 | 路径 | 说明 |
|--------|------|------|
| 1 | `$QQ_EMAIL_CONFIG` | 环境变量指定 |
| 2 | `./config.json` | Skill 目录下 |
| 3 | `~/.openclaw/email-config.json` | 向后兼容 |

### config.example.json

```json
{
  "email": "你的QQ邮箱@qq.com",
  "password": "QQ邮箱授权码",
  "smtp_server": "smtp.qq.com",
  "smtp_port": 465,
  "name": "发件人显示名称",
  "max_fetch": 10,
  "skip_keywords": ["noreply", "no-reply", "mailer-daemon"]
}
```

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `email` | ✅ | — | QQ 邮箱地址 |
| `password` | ✅ | — | 授权码（不是 QQ 密码） |
| `smtp_server` | ❌ | `smtp.qq.com` | SMTP 服务器 |
| `smtp_port` | ❌ | `465` | SMTP 端口 |
| `name` | ❌ | `AI助手` | 发件人显示名称 |
| `max_fetch` | ❌ | `10` | 默认读取数量 |
| `skip_keywords` | ❌ | 见示例 | 自动邮件过滤关键词 |

## 🔒 安全

编辑 `references/security.md` 自定义回复时的安全规则：

- 禁止泄露的信息类别（密钥、个人信息、系统信息等）
- 被问到敏感问题时的标准回复
- 高风险场景处理策略

## 📁 项目结构

```
qq-email-skill/
├── SKILL.md                 ← 使用文档
├── config.example.json      ← 配置模板
├── .gitignore               ← 排除敏感文件
├── LICENSE                  ← MIT
├── scripts/
│   ├── utils.py             ← 共享工具库
│   ├── setup.py             ← 配置验证 & 连接测试
│   ├── read_emails.py       ← 读取邮件
│   ├── reply_email.py       ← 发送回复
│   ├── manage_email.py      ← 标记管理
│   └── stats.py             ← 统计摘要
└── references/
    └── security.md          ← 安全守则（可自定义）
```

## ❓ 常见问题

<details>
<summary><b>IMAP 连接失败？</b></summary>

1. 确认已在 QQ 邮箱开启 IMAP/SMTP 服务
2. 使用授权码，不是 QQ 密码
3. 运行 `python3 scripts/setup.py` 诊断
</details>

<details>
<summary><b>回复被跳过了？</b></summary>

邮件 ID 已在 `replied.json` 中记录。用 `--force` 强制发送。
</details>

<details>
<summary><b>HTML 邮件正文乱码？</b></summary>

脚本自动将 HTML 转为纯文本。极少数复杂排版可能丢失格式。
</details>

<details>
<summary><b>怎么查看已发送邮件？</b></summary>

目前只支持收件箱。Sent 文件夹支持计划中。
</details>

## 🤝 贡献

欢迎 Issue 和 PR！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/xxx`)
3. 提交更改 (`git commit -m 'feat: add xxx'`)
4. 推送 (`git push origin feature/xxx`)
5. 开 Pull Request

## 📄 License

[MIT](LICENSE) © 2026
