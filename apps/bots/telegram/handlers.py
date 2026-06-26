from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from apps.bots.telegram.master_bot import bot
from apps.bots.models import BotUser, ChildBot

router = Router()


# هندلر استارت
@router.message(CommandStart())
async def start_handler(message: Message):
    chat_id = message.from_user.id
    username = message.from_user.username or ''
    first_name = message.from_user.first_name or ''

    # کاربر رو توی دیتابیس ذخیره یا پیدا کن
    user, created = await BotUser.objects.aget_or_create(
        chat_id=chat_id,
        defaults={
            'username': username,
            'first_name': first_name,
        }
    )

    if created:
        await message.answer(
            f"سلام {first_name} عزیز! 👋\n\n"
            f"به ربات‌ساز خوش اومدی!\n\n"
            f"برای ساخت ربات آپلودر خودت، توکن ربات تلگرامت رو بفرست."
        )
    else:
        await message.answer(
            f"سلام {first_name}! 👋\n\n"
            f"خوش برگشتی!\n\n"
            f"برای مدیریت ربانت از دستورات زیر استفاده کن:\n"
            f"/mybot - مشاهده ربات من\n"
            f"/help - راهنما"
        )


# هندلر راهنما
@router.message(Command('help'))
async def help_handler(message: Message):
    await message.answer(
        "راهنمای ربات‌ساز:\n\n"
        "۱. توکن ربات تلگرامت رو بفرست\n"
        "۲. ما ربات آپلودرت رو فعال میکنیم\n"
        "۳. فایل‌هات رو بفرست و لینک بگیر\n\n"
        "/mybot - مشاهده ربات من\n"
        "/help - راهنما"
    )


# هندلر مشاهده ربات
@router.message(Command('mybot'))
async def mybot_handler(message: Message):
    chat_id = message.from_user.id

    try:
        user = await BotUser.objects.aget(chat_id=chat_id)
        child_bot = await ChildBot.objects.aget(owner=user)

        status_emoji = '✅' if child_bot.status == 'active' else '❌'

        await message.answer(
            f"ربات تو:\n\n"
            f"نام: {child_bot.bot_name}\n"
            f"یوزرنیم: @{child_bot.username}\n"
            f"وضعیت: {status_emoji} {child_bot.get_status_display()}\n"
        )

    except BotUser.DoesNotExist:
        await message.answer("اول باید ثبت‌نام کنی! /start بزن.")

    except ChildBot.DoesNotExist:
        await message.answer(
            "هنوز ربات نداری!\n\n"
            "توکن ربات تلگرامت رو بفرست تا ربات آپلودرت رو بسازیم."
        )


# هندلر دریافت توکن
@router.message(F.text)
async def token_handler(message: Message):
    chat_id = message.from_user.id
    text = message.text.strip()

    # چک کن فرمت توکن درسته (عدد:حروف)
    if ':' not in text or not text.split(':')[0].isdigit():
        await message.answer(
            "متوجه نشدم! 🤔\n\n"
            "اگه میخوای ربات بسازی، توکن ربانت رو بفرست.\n"
            "توکن باید شبیه این باشه:\n"
            "<code>1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ</code>"
        )
        return

    # چک کن قبلاً ربات داره یا نه
    try:
        user = await BotUser.objects.aget(chat_id=chat_id)
        existing_bot = await ChildBot.objects.aget(owner=user)
        await message.answer(
            f"تو قبلاً یه ربات داری: @{existing_bot.username}\n\n"
            f"برای مدیریتش از /mybot استفاده کن."
        )
        return
    except (BotUser.DoesNotExist, ChildBot.DoesNotExist):
        pass

    # پیام در حال بررسی
    processing_msg = await message.answer("در حال بررسی توکن... ⏳")

    # توکن رو validate کن
    try:
        from aiogram import Bot as TempBot
        temp_bot = TempBot(token=text)
        bot_info = await temp_bot.get_me()
        await temp_bot.session.close()

        # کاربر رو پیدا یا بساز
        user, _ = await BotUser.objects.aget_or_create(
            chat_id=chat_id,
            defaults={
                'username': message.from_user.username or '',
                'first_name': message.from_user.first_name or '',
            }
        )

        # چک کن این توکن قبلاً ثبت نشده
        if await ChildBot.objects.filter(token=text).aexists():
            await processing_msg.edit_text("این توکن قبلاً ثبت شده! ❌")
            return

        # ربات رو توی دیتابیس ذخیره کن
        child_bot = await ChildBot.objects.acreate(
            owner=user,
            token=text,
            username=bot_info.username,
            bot_name=bot_info.first_name,
        )

        await processing_msg.edit_text(
            f"ربات آپلودرت با موفقیت ساخته شد! 🎉\n\n"
            f"نام: {bot_info.first_name}\n"
            f"یوزرنیم: @{bot_info.username}\n\n"
            f"در حال فعال‌سازی webhook..."
        )

        # webhook رو ست کن (مرحله بعد)
        # TODO: set webhook

        await message.answer(
            f"ربات @{bot_info.username} آماده‌ست! ✅\n\n"
            f"به زودی قابلیت آپلود فایل فعال میشه."
        )

    except Exception as e:
        await processing_msg.edit_text(
            "توکن نامعتبره! ❌\n\n"
            "مطمئن شو توکن رو درست کپی کردی."
        )