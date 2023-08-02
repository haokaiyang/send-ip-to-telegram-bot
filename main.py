import socket
from configparser import ConfigParser
from telegram import Bot
import asyncio

def get_internal_ip():
    return socket.gethostbyname(socket.gethostname())

def get_previous_ip():
    config = ConfigParser()
    config.read('config.ini')
    return config.get('IP', 'previous_ip')

def update_previous_ip(new_ip):
    config = ConfigParser()
    config.read('config.ini')
    config.set('IP', 'previous_ip', new_ip)
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

async def send_notification(message):
    config = ConfigParser()
    config.read('config.ini')
    bot_token = config.get('API', 'token')
    chat_id = config.get('API', 'chat_id')
    print(bot_token)
    print(chat_id)
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

async def main():
    # 读取配置文件中的 API token 和 chat ID
    config = ConfigParser()
    config.read('config.ini')

    previous_ip = get_previous_ip()
    current_ip = get_internal_ip()

    if previous_ip != current_ip:
        # IP 发生了变化，发送通知
        message = f"IP 已更新：{current_ip}"
        await send_notification(message)
        update_previous_ip(current_ip)
    else:
        # IP 没有变化
        message = "IP 没有变化"
        await send_notification(message)

async def run_main():
    # 在这个异步函数中调用 main() 函数，并等待其执行完成
    await main()

# 创建异步事件循环并运行主函数
loop = asyncio.get_event_loop()
loop.run_until_complete(run_main())


