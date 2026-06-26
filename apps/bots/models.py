from django.db import models
import secrets


class BotUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)

    is_admin = models.BooleanField(default=False)

    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} (@{self.username})" if self.username else str(self.chat_id)


class ChildBot(models.Model):
    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
        ('error', 'خطا در توکن'),
    ]

    owner = models.OneToOneField(BotUser, on_delete=models.CASCADE, related_name='bot')

    token = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, blank=True)
    bot_name = models.CharField(max_length=100, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    webhook_set = models.BooleanField(default=False)

    # متن استارت که برای کاربرای بات نمایش داده میشه
    welcome_text = models.TextField(blank=True, default='سلام! خوش اومدی 👋')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"@{self.username}" if self.username else self.token[:10]


class SharedFile(models.Model):
    FILE_TYPES = [
        ('photo', 'عکس'),
        ('video', 'ویدیو'),
        ('document', 'فایل'),
        ('audio', 'صدا'),
        ('voice', 'ویس'),
        ('animation', 'گیف'),
    ]

    bot = models.ForeignKey(ChildBot, on_delete=models.CASCADE, related_name='files')

    slug = models.CharField(max_length=32, unique=True, editable=False)

    file_id = models.CharField(max_length=255)
    file_unique_id = models.CharField(max_length=100, blank=True)
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    file_name = models.CharField(max_length=255, blank=True)
    caption = models.TextField(blank=True)

    view_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = secrets.token_urlsafe(8)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file_type} - {self.slug}"