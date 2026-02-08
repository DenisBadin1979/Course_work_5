from symtable import Class

from django.db import models

class Habit (models.Model):


    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
    pass

class Place (models.Model):


    class Meta:
        verbose_name = "Место действия"
        verbose_name_plural = "Места действия"

    pass

class Award (models.Model):

    class Meta:
        verbose_name = "Вознаграждение"
        verbose_name_plural = "Вознаграждения"

    pass
