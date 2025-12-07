import discord
import os
import requests
from flask import Flask
from threading import Thread
import asyncio

# --- Monkey Patch: 修复 discord.py-self 1.9.2 在 Replit 上的兼容性问题 ---
# 解决 friend_source_flags 报错
import discord.settings
original_from_dict = discord.settings.FriendFlags._from_dict

def patched_from_dict(data):
    if data is None:
        return discord.settings.FriendFlags()
    return original_from_dict(data)

discord.settings.FriendFlags._from_dict = patched_from_dict
# ------------------------------------------------------------------

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
# 优先从环境变量读取，确保 Token 安全
USER_TOKEN = os.getenv('USER_TOKEN')
TARGET_USER_ID = os.getenv('TARGET_USER_ID')
TARGET_CHANNEL_ID = os.getenv('TARGET_CHANNEL_ID')
NOTIFY_URL = os.getenv('NOTIFY_URL')

# 数据类型转换
if TARGET_USER_ID: TARGET_USER_ID = int(TARGET_USER_ID)
if TARGET_CHANNEL_ID: TARGET_CHANNEL_ID = int(TARGET_CHANNEL_ID)

# --- 3. Discord Client ---
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'✅ Monitor Started! Logged in as: {self.user}')
        print(f'Listening to user {TARGET_USER_ID} in channel {TARGET_CHANNEL_ID}...')

    async def on_message(self, message):
        # 排除自身消息
        if message.author == self.user:
            return

        # 频道与用户筛选
        if message.channel.id == TARGET_CHANNEL_ID and message.author.id == TARGET_USER_ID:
            content = message.content
            print(f"⚠️ Captured Message: {content}")
            
            # 推送通知
            try:
                full_url = f"{NOTIFY_URL}【Monitor】{content}"
                requests.get(full_url)
                print("🚀 Notification Sent")
            except Exception as e:
                print(f"❌ Notification Failed: {e}")

# --- 4. 启动逻辑 ---
if __name__ == '__main__':
    keep_alive()
    
    if USER_TOKEN:
        print("Logging in...")
        client = MyClient()
        client.run(USER_TOKEN)
    else:
        print("❌ Error: USER_TOKEN not found in environment variables.")