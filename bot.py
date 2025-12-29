from telethon import TelegramClient, events
from telethon.tl.types import MessageEntityBold
import asyncio
from datetime import datetime

# اطلاعات مربوط به اکانت خود را وارد کنید
api_id = '5888972'
api_hash = '8c6c75ac3bb436c548e56e93020cb738'
source_channel = '@NerkhYab_Khorasan'  # کانال مبدا
destination_channel = '@SRAFI_HERAT'  # کانال مقصد

# تنظیمات ربات - باید global تعریف شوند
bot_status = "on"  # وضعیت ربات: "on" یا "off"
admins = [5734726593]  # لیست ادمین‌ها (ایدی عددی)

# لیست کلمات فیلتر شده
filtered_words = ['@', 'https', 't.me', 'بازار', 'دلار', 'هزینه', 'رایگان', 'vip', 'VIP', 'آموزش', '✅️', 'همگی', 'مکتب', 'شماره', 'ثبت', 'ایا', 'خبر', 'زشت']

# پیام جایگزین کلمات فیلتر
replacement_message = "*بِسْــــــــــــــــــمِ ﷲِالرَّحْمَنِ الرَّحِيم*\n\n\n*إِنَّ اللَّهَ وَمَلائِكَتَهُ يُصَلُّونَ عَلَى النَّبِيِّ يَا أَيُّهَا الَّذِينَ آمَنُوا صَلُّوا عَلَيْهِ وَسَلِّمُوا تَسْلِيمًا*\n\n*اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ كَمَا صَلَّيْتَ عَلَى إِبْرَاهِيمَ وَعَلَى آلِ إِبْرَاهِيمَ إِنَّكَ حَمِيدٌ مَجِيدٌ*\n\n\n*اللَّهُمَّ بَارِكْ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ كَمَا بَارَكْتَ عَلَى إِبْرَاهِيمَ وَعَلَى آلِ إِبْرَاهِيمَ إِنَّكَ حَمِيدٌ مَجِيدٌ*"

# آمار ربات
stats = {
    'total_messages': 0,
    'filtered_messages': 0,
    'forwarded_messages': 0,
    'start_time': None
}

client = TelegramClient('session_name', api_id, api_hash)

# هندلر برای پیام‌های خصوصی (دستورات)
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def private_message_handler(event):
    # متغیرهای global
    global bot_status
    
    # بررسی اینکه آیا پیام از ادمین است
    sender_id = event.sender_id
    
    if sender_id not in admins:
        await event.reply("⛔ شما دسترسی ندارید!")
        return
    
    message_text = event.message.message.lower().strip() if event.message.message else ""
    
    if message_text == "وضعیت":
        # محاسبه زمان فعالیت
        if stats['start_time']:
            uptime = datetime.now() - stats['start_time']
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{uptime.days} روز, {hours} ساعت, {minutes} دقیقه, {seconds} ثانیه"
        else:
            uptime_str = "اطلاعاتی موجود نیست"
        
        # ساخت پیام وضعیت
        status_icon = "🟢" if bot_status == "on" else "🔴"
        status_text = "**روشن**" if bot_status == "on" else "**خاموش**"
        
        status_message = f"""
{status_icon} **وضعیت ربات**

**📊 آمار:**
├ کل پیام‌ها: {stats['total_messages']}
├ پیام‌های فوروارد شده: {stats['forwarded_messages']}
├ پیام‌های فیلتر شده: {stats['filtered_messages']}
└ زمان فعالیت: {uptime_str}

**⚙️ تنظیمات:**
├ وضعیت: {status_text}
├ کانال مبدا: {source_channel}
├ کانال مقصد: {destination_channel}
└ کلمات فیلتر: {len(filtered_words)} کلمه

**📋 دستورات:**
├ وضعیت - نمایش وضعیت ربات
├ روشن - روشن کردن ربات
├ خاموش - خاموش کردن ربات
└ کلمات - نمایش کلمات فیلتر شده
"""
        await event.reply(status_message)
    
    elif message_text == "روشن":
        if bot_status == "on":
            await event.reply("✅ ربات از قبل **روشن** است.")
        else:
            bot_status = "on"
            await event.reply("✅ ربات **روشن** شد.")
    
    elif message_text == "خاموش":
        if bot_status == "off":
            await event.reply("✅ ربات از قبل **خاموش** است.")
        else:
            bot_status = "off"
            await event.reply("✅ ربات **خاموش** شد.")
            stats['start_time'] = None
    
    elif message_text == "کلمات":
        if filtered_words:
            words_list = "\n".join([f"{i+1}. `{word}`" for i, word in enumerate(filtered_words)])
            await event.reply(f"**📋 کلمات فیلتر شده:**\n{words_list}")
        else:
            await event.reply("📭 لیست کلمات فیلتر شده خالی است.")
    
    elif message_text == "آمار":
        await event.reply(f"""
📊 **آمار ربات:**
├ کل پیام‌ها: {stats['total_messages']}
├ پیام‌های فوروارد شده: {stats['forwarded_messages']}
└ پیام‌های فیلتر شده: {stats['filtered_messages']}
""")
    
    elif message_text.startswith("افزودن "):
        if len(message_text.split()) > 1:
            new_word = message_text.split(" ", 1)[1]
            if new_word in filtered_words:
                await event.reply(f"⚠️ کلمه `{new_word}` از قبل در لیست فیلتر وجود دارد.")
            else:
                filtered_words.append(new_word)
                await event.reply(f"✅ کلمه `{new_word}` به لیست فیلتر اضافه شد.")
        else:
            await event.reply("⚠️ لطفاً کلمه را بعد از 'افزودن' وارد کنید.\nمثال: `افزودن تبلیغ`")
    
    elif message_text.startswith("حذف "):
        if len(message_text.split()) > 1:
            word_to_remove = message_text.split(" ", 1)[1]
            if word_to_remove in filtered_words:
                filtered_words.remove(word_to_remove)
                await event.reply(f"✅ کلمه `{word_to_remove}` از لیست فیلتر حذف شد.")
            else:
                await event.reply(f"⚠️ کلمه `{word_to_remove}` در لیست فیلتر وجود ندارد.")
        else:
            await event.reply("⚠️ لطفاً کلمه را بعد از 'حذف' وارد کنید.\nمثال: `حذف تبلیغ`")
    
    elif message_text == "راهنما":
        help_text = """
📖 **راهنمای دستورات:**

**📊 وضعیت** - نمایش وضعیت کامل ربات
**🔘 روشن** - روشن کردن ربات
**🔘 خاموش** - خاموش کردن ربات
**📋 کلمات** - نمایش لیست کلمات فیلتر
**📊 آمار** - نمایش آمار ربات
**➕ افزودن [کلمه]** - افزودن کلمه به فیلتر
**➖ حذف [کلمه]** - حذف کلمه از فیلتر
**📖 راهنما** - نمایش این پیام

**مثال:**
`افزودن اسپم`
`حذف vip`
"""
        await event.reply(help_text)

# هندلر اصلی برای پیام‌های کانال
@client.on(events.NewMessage(chats=source_channel))
async def channel_message_handler(event):
    # آپدیت آمار
    stats['total_messages'] += 1
    
    # اگر ربات خاموش است، کاری نکن
    if bot_status == "off":
        return
    
    message_text = event.message.message or ""
    
    # تنظیم زمان شروع فعالیت
    if stats['start_time'] is None:
        stats['start_time'] = datetime.now()
    
    # بررسی کلمات فیلتر
    contains_filtered_word = any(word in message_text for word in filtered_words)
    
    if contains_filtered_word:
        stats['filtered_messages'] += 1
        print(f"پیام فیلتر شده: {message_text[:50]}...")
        
        # ارسال پیام جایگزین
        await client.send_message(destination_channel, replacement_message)
        stats['forwarded_messages'] += 1
    else:
        # فوروارد پیام اصلی
        if event.message.media:
            await client.send_message(destination_channel, event.message)
        else:
            await client.send_message(destination_channel, message_text)
        stats['forwarded_messages'] += 1

async def main():
    await client.start()
    
    # گرفتن اطلاعات اکانت
    me = await client.get_me()
    print(f"✅ ربات با موفقیت راه‌اندازی شد!")
    print(f"👤 اکانت: {me.first_name} ({me.username})")
    print(f"📥 کانال مبدا: {source_channel}")
    print(f"📤 کانال مقصد: {destination_channel}")
    print(f"🔘 وضعیت: {bot_status}")
    print(f"👥 ادمین‌ها: {len(admins)} نفر")
    print(f"📋 کلمات فیلتر: {len(filtered_words)} کلمه")
    print("\n📡 در حال گوش دادن به پیام‌ها...")
    print("=" * 50)
    
    # ارسال پیام شروع به ادمین‌ها
    for admin_id in admins:
        try:
            await client.send_message(
                admin_id,
                f"🤖 **ربات راه‌اندازی شد!**\n\n"
                f"🟢 وضعیت: **{bot_status}**\n"
                f"📥 کانال مبدا: `{source_channel}`\n"
                f"📤 کانال مقصد: `{destination_channel}`\n\n"
                f"برای مشاهده دستورات، **راهنما** را ارسال کنید."
            )
        except Exception as e:
            print(f"⚠️ خطا در ارسال پیام به ادمین {admin_id}: {e}")
    
    await client.run_until_disconnected()

# اجرای ربات
if __name__ == "__main__":
    try:
        print("🚀 در حال راه‌اندازی ربات...")
        with client:
            client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n\n⏹️ ربات متوقف شد.")
    except Exception as e:
        print(f"❌ خطا در اجرای ربات: {e}")
