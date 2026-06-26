from django.urls import path
from .views import MasterBotWebhookView

urlpatterns = [
    path('master/', MasterBotWebhookView.as_view(), name='master-webhook'),
]