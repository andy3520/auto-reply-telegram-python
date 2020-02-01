from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.types import UserStatusOffline, UserStatusOnline
import asyncio
import time
from telethon import events
from datetime import datetime

api_id = '1021645'
api_hash = 'c9519acb40e96eeb136be957f670dfbf'
user_name = 'butterrrr'

# client = TelegramClient(user_name, api_id, api_hash)
with TelegramClient(user_name, api_id, api_hash) as client:
    result = client(UpdateStatusRequest(
        offline=True
    ))
    print(datetime.now(), 'Chạy auto reply thành công')

message = 'Trả lời tự động: Hiện tại tôi đang bận, tôi sẽ trả lời ngay khi online'


def main():

    client.start()

    @client.on(events.NewMessage(incoming=True))
    async def _(event):
        print(datetime.now(), 'Nhận được 1 tin nhắn với nội dung', event.message.message)
        me = await client.get_me()
        from_ = await event.client.get_entity(event.from_id)
        print(f'{me.status}| {me.status.expires}' if isinstance(me.status, UserStatusOnline) else me.status)
        if event.is_private and not from_.bot:
            if isinstance(me.status, UserStatusOffline):
                time.sleep(1)  # pause for 1 second to rate-limit automatic replies
                await client.send_message(event.message.from_id, message)
                await client(UpdateStatusRequest(offline=True))
                print(datetime.now(), 'Đã trả lời')

    client.run_until_disconnected()


if __name__ == '__main__':
    main()
