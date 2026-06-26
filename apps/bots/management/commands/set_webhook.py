import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.bots.telegram.master_bot import bot


class Command(BaseCommand):
    help = 'ست کردن webhook مستر بات'

    def handle(self, *args, **kwargs):
        asyncio.run(self.set_webhook())

    async def set_webhook(self):
        webhook_url = f"{settings.WEBHOOK_BASE_URL}/webhook/master/"

        await bot.set_webhook(
            url=webhook_url,
            drop_pending_updates=True,
        )

        info = await bot.get_webhook_info()

        if info.url == webhook_url:
            self.stdout.write(
                self.style.SUCCESS(f"webhook با موفقیت ست شد:\n{webhook_url}")
            )
        else:
            self.stdout.write(
                self.style.ERROR("خطا در ست کردن webhook!")
            )

        await bot.session.close()