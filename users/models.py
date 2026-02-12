from django.contrib.auth.models import AbstractUser
from django.db import models
from mypy.dmypy_server import AbstractSet


class User(AbstractUser):
    tg_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Chat_ID из telegram",
        help_text="Введите имя оChat_ID",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
