import discord
import os
import requests
from flask import Flask
from threading import Thread
import asyncio
import time  # 新增: 用于等待重连
import sys   # 新增: 用于处理系统退出

# --- 1. Web Server (端口 8080) ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive! Running on Tencent Cloud."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. 配置加载 ---
USER_TOKEN = os.getenv('USER_TOKEN')
TARGET_USER_ID = os.getenv('TARGET_USER_ID')
TARGET_CHANNEL_ID = os.getenv('TARGET_CHANNEL_ID')
NOTIFY_URL = os.getenv('NOTIFY_URL')

# 类型转换
if TARGET_USER_ID: TARGET_USER_ID = int(TARGET_USER_ID)
if TARGET_CHANNEL_ID: TARGET_CHANNEL_ID = int(TARGET_CHANNEL_ID)

# --- 3. Discord Client ---
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'✅ 监控已启动！登录账号: {self.user}')

        # === 核心修改：主动验证连接 ===
        try:
            # 尝试获取频道信息
            channel = self.get_channel(TARGET_CHANNEL_ID)
            if channel:
                print(f"🎉 验证成功！已连接到频道: 【{channel.name}】")
                print(f"   频道ID: {channel.id}")
                # 尝试读取最后一条消息ID来确认权限
                if hasattr(channel, 'last_message_id'):
                    print(f"   权限检查: 可读取历史消息 (Last Msg ID: {channel.last_message_id})")
            else:
                print(f"❌ 警告: 无法找到频道 {TARGET_CHANNEL_ID}")
                print("   可能原因: 1.ID填错 2.账号不在该群 3.被踢出")
        except Exception as e:
            print(f"❌ 验证过程报错: {e}")
        # ===========================

        print(f'正在监听频道 {TARGET_CHANNEL_ID} 中用户 {TARGET_USER_ID} 的发言...')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.id == TARGET_CHANNEL_ID and message.author.id == TARGET_USER_ID:
            content = message.content
            print(f"⚠️ 捕获到目标发言: {content}")
            
            try:
                full_url = f"{NOTIFY_URL}【华尔街阿宝_主频道】{content}"
                requests.get(full_url)
                print("🚀 通知已推送到手机")
            except Exception as e:
                print(f"❌ 推送失败: {e}")

# --- 4. 启动 (新增自动重连机制) ---
if __name__ == '__main__':
    keep_alive()
    
    if not USER_TOKEN:
        print("❌ 错误: 环境变量丢失，请检查 start.sh")
        sys.exit(1)

    print("🚀 程序主循环已启动...")
    
    # === 这里是修改的重点：死循环守护 ===
    while True:
        try:
            print("\n🔄 正在连接 Discord 服务器...")
            # 每次重连创建一个新的 Client 实例，防止旧实例状态残留
            client = MyClient()
            client.run(USER_TOKEN)
        except Exception as e:
            print(f"\n❌ 发生错误 (连接断开/网络波动): {e}")
            print("⏳ 10秒后自动尝试重连...")
            time.sleep(10)  # 休息10秒，避免请求过快被封IP
        except KeyboardInterrupt:
            print("\n👋 用户手动停止程序")
            sys.exit(0)
