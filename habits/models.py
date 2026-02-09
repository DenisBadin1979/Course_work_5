from symtable import Class

from django.db import models


class Habit(models.Model):

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    pass


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


class Award(models.Model):

    class Meta:
        verbose_name = "Вознаграждение"
        verbose_name_plural = "Вознаграждения"

    pass
