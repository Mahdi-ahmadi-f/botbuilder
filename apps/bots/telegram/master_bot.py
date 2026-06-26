from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from django.conf import settings

# بات اصلی
bot = Bot(
    token=settings.MASTER_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# دیسپچر
dp = Dispatcher()