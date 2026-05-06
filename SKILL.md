---
name: qq-email
description: QQ邮箱智能邮件助手。读取未读邮件、分析内容、自主回复、标记管理。触发词：邮件、邮箱、未读邮件、回复邮件、查邮件、email。
---

# QQ 邮箱 Skill

为 AI Agent 提供 QQ 邮箱的读取、分析、回复能力。

## 快速开始

### 1. 获取 QQ 邮箱授权码

1. 登录 [QQ 邮箱](https://mail.qq.com)
2. 设置 → 账户 → POP3/IMAP/SMTP 服务
3. 开启 IMAP/SMTP 服务
4. 生成授权码（不是 QQ 密码）

### 2. 配置

```bash
cp config.example.json config.json
# 编辑 config.json 填写邮箱和授权码
```

### 3. 验证配置

```bash
python3 scripts/setup.py
```

自动检查配置完整性、IMAP/SMTP 连接、收件箱状态。

## 使用方法

### 读取邮件

```bash
python3 scripts/read_emails.py                    # 默认读取最新未读
python3 scripts/read_emails.py --limit 5          # 指定数量
python3 scripts/read_emails.py --from "boss@xx.com" # 按发件人过滤
python3 scripts/read_emails.py --subject "会议"    # 按主题过滤
python3 scripts/read_emails.py --days 3           # 最近 N 天（高效）
python3 scripts/read_emails.py --all              # 包含已读
python3 scripts/read_emails.py --raw              # 不截断正文
```

`--days` 使用 IMAP 原生搜索，不会全量拉取邮件，大邮箱也很快。

### 回复邮件

```bash
python3 scripts/reply_email.py \
  --to "sender@example.com" \
  --subject "Re: 原主题" \
  --body "回复内容" \
  --in-reply-to "<原邮件Message-ID>"
```

- 自动记录到 `replied.json`，避免重复回复
- 使用 `--force` 跳过重复检查

### 管理邮件

```bash
python3 scripts/manage_email.py --action read --nums "1,2,3"
python3 scripts/manage_email.py --action unread --nums "1,2,3"
python3 scripts/manage_email.py --action read-all
python3 scripts/manage_email.py --action delete --nums "1,2,3"
```

### 收件箱统计

```bash
python3 scripts/stats.py              # 最近 7 天统计
python3 scripts/stats.py --days 30    # 最近 30 天
python3 scripts/stats.py --top 5      # Top 5 排行
```

输出：总邮件数、未读数、近期数量、Top 发件人、热门主题。

## 配置

### 配置查找顺序

1. 环境变量 `QQ_EMAIL_CONFIG` 指定的路径
2. Skill 目录下的 `config.json`
3. `~/.openclaw/email-config.json`（向后兼容）

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

## 回复规则

1. **先读 `references/security.md`** — 每次回复前检查安全守则
2. **理解内容再回复** — 不用模板，分析邮件意图后针对性回复
3. **不泄露敏感信息** — 按 security.md 中的规则过滤
4. **语气自然** — 像真人写邮件
5. **不确定就不回** — 拿不准的邮件标记未读

## 常见问题排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `找不到配置文件` | 没有 config.json | `cp config.example.json config.json` |
| `JSON 格式错误` | config.json 语法错误 | 检查逗号、引号，用 JSON 校验器 |
| `IMAP 连接失败` | 授权码错误或未开启 IMAP | 去 QQ 邮箱重新生成授权码 |
| `SMTP 连接失败` | 端口或服务器错误 | 确认 smtp.qq.com:465 |
| `没有未读邮件` | 确实没有未读 | 用 `--all` 查看所有邮件 |
| `回复被跳过` | replied.json 有记录 | 用 `--force` 强制发送 |
| `邮件正文为空` | 只有 HTML 且解析失败 | 代码自动尝试 HTML→文本，极少数情况仍可能为空 |
| `授权码无效` | 过期或被重置 | 重新在 QQ 邮箱生成授权码 |
| `连接超时` | 网络问题 | 检查网络，脚本会自动重试 3 次 |
| `权限不足` | QQ 邮箱未开启 IMAP | 设置 → 账户 → 开启 IMAP/SMTP |

## 文件结构

```
qq-email/
├── SKILL.md                ← 本文件
├── config.example.json     ← 配置模板
├── .gitignore              ← 排除 config.json
├── LICENSE                 ← MIT
├── scripts/
│   ├── utils.py            ← 共享工具库（重试、解码、HTML转换、IMAP搜索）
│   ├── setup.py            ← 配置验证 & 连接测试
│   ├── read_emails.py      ← 读取邮件（支持过滤）
│   ├── reply_email.py      ← 发送回复（含重复检查）
│   ├── manage_email.py     ← 标记/删除管理
│   └── stats.py            ← 收件箱统计摘要
└── references/
    └── security.md         ← 安全守则（可自定义）
```

## 依赖

Python 3.7+（仅使用标准库，无需额外安装）

## License

MIT
