# Discord User Monitor (Self-Bot) | Discord 用户实时监控机器人

这是一个基于 Python 的轻量级 Discord 监控脚本。它部署在云端 Replit ，通过 UptimeRobot 实现 24/7 全天候运行。

主要功能是实时监控指定 Discord 频道中的特定用户发言，并即时推送到你的手机。

## 🚀 功能特性

- 实时监控：毫秒级捕获指定用户的聊天信息。
- 多端推送：支持 Bark (iOS)、Telegram Bot 或任意 HTTP Webhook 推送。
- 云端保活：内置 Flask Web Server，配合 UptimeRobot 防止云容器休眠。
- Replit 兼容：已修复 `discord.py-self` 库在 Replit 环境下的兼容性问题（Monkey Patch）。

## 🛠️ 环境要求

1.  Discord User Token (用户 Token，非机器人 Token)。
2.  Python 3.8+。
3.  目标用户的 ID 和所在频道 ID。

## ⚙️ 环境变量配置

⚠️ 安全警告：请勿将 Token 直接写入代码中！请使用环境变量 (Secrets) 管理。

在 Replit 的 `Secrets` 面板或本地 `.env` 文件中配置以下变量：

| 变量名 (Key) | 说明 (Description) | 示例 |
| :--- | :--- | :--- |
| `USER_TOKEN` | 你的 Discord 用户 Token | `OTMzNj...` |
| `TARGET_USER_ID` | 被监控的用户 ID | `123456789...` |
| `TARGET_CHANNEL_ID` | 监控所在的频道 ID | `987654321...` |
| `NOTIFY_URL` | 消息推送的 API 地址 | `https://api.day.app/KEY/` |

## 📦 部署指南 (Replit + UptimeRobot)

### 1. 部署代码
1.  在 [Replit](https://replit.com/) 创建一个新的 Python 项目。
2.  将仓库中的 `main.py` 导入项目。
3.  在 Secrets 面板添加上述环境变量。
4.  在 Shell 中重装正确的库
    卸载所有 Discord 相关库：pip uninstall discord discord.py discord.py-self -y  (多运行一次也无妨，确保删干净)
    安装 GitHub 最新版 ：pip install git+https://github.com/dolfies/discord.py-self.git
5.  点击 Run 运行脚本。

### 2. 配置保活
1.  脚本运行后，复制 Replit 右上角 Webview 的地址（例如 `https://project.user.replit.dev`）。
2.  注册并登录 [UptimeRobot](https://uptimerobot.com/)。
3.  点击 Add New Monitor，类型选择 HTTP(s)。
4.  URL 填入刚才复制的地址，频率设置为 5分钟。
5.  保存即可，脚本现已支持 24 小时后台运行。

## ⚠️ 免责声明 (Disclaimer)

本项目使用了 `discord.py-self` 库来自动化个人账号（Self-Bot）。
自动化个人账号违反了 Discord 的服务条款 (ToS)。
使用本项目产生的风险（如账号被封禁）由使用者自行承担。

## 📄 开源协议


MIT License
