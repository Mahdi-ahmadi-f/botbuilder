from django.contrib import admin
from .models import BotUser, ChildBot, SharedFile


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'username', 'first_name', 'is_admin', 'joined_at']
    list_filter = ['is_admin']
    search_fields = ['chat_id', 'username']


@admin.register(ChildBot)
class ChildBotAdmin(admin.ModelAdmin):
    list_display = ['username', 'owner', 'status', 'webhook_set', 'created_at']
    list_filter = ['status', 'webhook_set']
    search_fields = ['username', 'bot_name']


@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ['slug', 'bot', 'file_type', 'file_name', 'view_count', 'created_at']
    list_filter = ['file_type', 'bot']
    search_fields = ['slug', 'file_name']