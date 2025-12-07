import discord
import os
import requests
from flask import Flask
from threading import Thread
import asyncio

# --- 1. Web Server for UptimeRobot (保活服务) ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive! Monitoring..."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. 配置加载 ---
# 优先从环境变量读取
USER_TOKEN = os.getenv('USER_TOKEN')
TARGET_USER_ID = os.getenv('TARGET_USER_ID')
TARGET_CHANNEL_ID = os.getenv('TARGET_CHANNEL_ID')
NOTIFY_URL = os.getenv('NOTIFY_URL')

# 数据类型转换 (防止环境变量读不到导致报错)
if TARGET_USER_ID: TARGET_USER_ID = int(TARGET_USER_ID)
if TARGET_CHANNEL_ID: TARGET_CHANNEL_ID = int(TARGET_CHANNEL_ID)

# --- 3. Discord Client ---
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'✅ 监控已启动！登录账号: {self.user}')
        print(f'正在监听频道 {TARGET_CHANNEL_ID} 中用户 {TARGET_USER_ID} 的发言...')

    async def on_message(self, message):
        # 1. 排除自身消息 (防死循环)
        if message.author == self.user:
            return

        # 2. 频道与用户筛选
        if message.channel.id == TARGET_CHANNEL_ID and message.author.id == TARGET_USER_ID:
            content = message.content
            print(f"⚠️ 捕获到目标发言: {content}")

            # 3. 推送通知
            try:
                full_url = f"{NOTIFY_URL}【大神更新】{content}"
                requests.get(full_url)
                print("🚀 通知已推送到手机")
            except Exception as e:
                print(f"❌ 推送失败: {e}")

# --- 4. 启动逻辑 ---
if __name__ == '__main__':
    keep_alive()

    if USER_TOKEN:
        print("正在尝试登录...")
        # 新版库通常不需要手动传 intents，直接实例化即可
        client = MyClient()
        client.run(USER_TOKEN)
    else:
        print("❌ 错误: 未找到 USER_TOKEN，请检查 Secrets 配置。")
