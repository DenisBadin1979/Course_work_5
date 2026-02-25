import requests
from celery import shared_task


from config.settings import TELEGRAM_TOKEN, TELEGRAM_URL
from habits.models import Habit


@shared_task
def some_task_1d():
    for hab in Habit.objects.all():
        if hab.is_pleasant is False and hab.periodicity == 1:
            msg = f"Ваша полезная привычка {hab.action} должна быть выполнена сегодня {hab.time}"
            chat_id = hab.user.tg_chat_id
            params = {"text": msg, "chat_id": chat_id}
            requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)


@shared_task
def some_task_2d():
    for hab in Habit.objects.all():
        if hab.is_pleasant is False and hab.periodicity == 2:
            msg = f"Ваша полезная привычка {hab.action} должна быть выполнена сегодня {hab.time}"
            chat_id = hab.user.tg_chat_id
            params = {"text": msg, "chat_id": chat_id}
            requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)


@shared_task
def some_task_3d():
    for hab in Habit.objects.all():
        if hab.is_pleasant is False and hab.periodicity == 3:
            msg = f"Ваша полезная привычка {hab.action} должна быть выполнена сегодня {hab.time}"
            chat_id = hab.user.tg_chat_id
            params = {"text": msg, "chat_id": chat_id}
            requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)


@shared_task
def some_task_4d():
    for hab in Habit.objects.all():
        if hab.is_pleasant is False and hab.periodicity == 4:
            msg = f"Ваша полезная привычка {hab.action} должна быть выполнена сегодня {hab.time}"
            chat_id = hab.user.tg_chat_id
            params = {"text": msg, "chat_id": chat_id}
            requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)


@shared_task
def some_task_5d():
    for hab in Habit.objects.all():
        if hab.is_pleasant is False and hab.periodicity == 5:
            msg = f"Ваша полезная привычка {hab.action} должна быть выполнена сегодня {hab.time}"
            chat_id = hab.user.tg_chat_id
            params = {"text": msg, "chat_id": chat_id}
            requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)


@shared_task
def some_task_6d():
    for hab in Habit.objects.all():
        if hab.is_pleasant is False and hab.periodicity == 6:
            msg = f"Ваша полезная привычка {hab.action} должна быть выполнена сегодня {hab.time}"
            chat_id = hab.user.tg_chat_id
            params = {"text": msg, "chat_id": chat_id}
            requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)


@shared_task
def some_task_7d():
    for hab in Habit.objects.all():
        if hab.is_pleasant is False and hab.periodicity == 7:
            msg = f"Ваша полезная привычка {hab.action} должна быть выполнена сегодня {hab.time}"
            chat_id = hab.user.tg_chat_id
            params = {"text": msg, "chat_id": chat_id}
            requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)
