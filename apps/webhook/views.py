import json
import logging

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from aiogram.types import Update

from apps.bots.telegram.master_bot import bot, dp
from apps.bots.telegram.handlers import router

logger = logging.getLogger(__name__)

# روتر رو به دیسپچر وصل کن
dp.include_router(router)


@method_decorator(csrf_exempt, name='dispatch')
class MasterBotWebhookView(View):

    async def post(self, request):
        print(">>>>>> درخواست رسید <<<<<<")
        logger.error(">>>>>> درخواست رسید <<<<<<")
        try:
            data = json.loads(request.body)
            update = Update(**data)
            await dp.feed_update(bot=bot, update=update)
            return JsonResponse({'ok': True})

        except Exception as e:
            logger.error(f"خطا در پردازش آپدیت: {e}")
            return JsonResponse({'ok': False}, status=500)