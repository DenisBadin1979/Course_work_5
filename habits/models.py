from django.db import models
from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    place = models.ForeignKey(
        "Place",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Выберите место",
    )
    award = models.ForeignKey(
        "Award",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Выберите вознаграждение",
    )
    action = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Действие - привычка",
        help_text="Укажите само действие - привычку",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Укажите является ли действие - привычка приятной привычки",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Указывается только для полезных привычек. Не может быть приятной привычкой.",
        related_name="pleasant_rewards",
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (дни)",
        blank=True,
        null=True,
    )
    duration = models.PositiveIntegerField(
        help_text="Время на выполнение в секундах", blank=True, null=True
    )
    time = models.TimeField(
        verbose_name="Время",
        help_text="Укажите в какое время будет осуществляться привычка",
        blank=True,
        null=True,
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичная",
        help_text="Укажите что привычка публичная",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["action", "place"]

    def __str__(self):
        return self.action


class Place(models.Model):
    location = models.CharField(
        max_length=50,
        verbose_name="Название локации",
        help_text="Введите название места : например, работа. дом. пляж, улица и т.д.",
    )
    clarifying = models.TextField(
        verbose_name="Описание (уточнение) места действия",
        help_text="Детально уточните места действия: беговая дорожка в зале, на коврике в комнате и т.д.",
    )

    class Meta:
        verbose_name = "Место действия"
        verbose_name_plural = "Места действия"
        ordering = ["location"]

    def __str__(self):
        return self.location


class Award(models.Model):
    award = models.CharField(
        max_length=50,
        verbose_name="Название вознаграждения",
        help_text="Вознаграждение — чем пользователь должен себя вознаградить после выполнения.",
    )
    description = models.TextField(
        verbose_name="Описание (уточнение) места действия",
        help_text="Детально уточните места действия: беговая дорожка в зале, на коврике в комнате и т.д.",
    )

    class Meta:
        verbose_name = "Вознаграждение"
        verbose_name_plural = "Вознаграждения"
        ordering = ["award"]

    def __str__(self):
        return self.award
