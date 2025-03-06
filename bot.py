# Mir
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime
import asyncio

# اطلاعات مربوط به API
api_id = '26495693'
api_hash = 'a3ffc595687a857608f2f2cd3c1c99d8'
phone_number = '+989335865143'

# ایجاد کلاینت تلگرام
client = TelegramClient('session_name', api_id, api_hash)

async def update_last_name():
    await client.start()
    
    while True:
        # گرفتن زمان فعلی
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # تغییر نام خانوادگی
        await client(UpdateProfileRequest(last_name=current_time))
        
        # نمایش زمان به صورت لحظه‌ای در کنسول
        print(f"Last name changed to: {current_time}", end='\r')
        
        # خوابیدن به مدت یک ثانیه
        await asyncio.sleep(1)

with client:
    client.loop.run_until_complete(update_last_name())
