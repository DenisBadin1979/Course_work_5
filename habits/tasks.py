from celery import shared_task
import requests
from habits.models import Habit


# @shared_task
def some_task_1d():
    for hab in Habit.objects.all():
        if hab.is_pleasant == False and hab.periodicity ==1:
            msg = f"Ваша полезная привычка {hab.action} должна быть выполнена сегодня {hab.time}"
            chat_id = hab.user.tg_chat_id
            params = {
                      "text" : msg,
                      "chat_id" : chat_id
                      }
            requests.get(r'https://api.telegram.org/bot{}/sendMessage?chat_id={}}&text=Привет!')
            print(msg)
    return None






    # https: // api.telegram.org / bot123456: ABC - DEF1234ghIkl - zyx57W2v1u12345678 / sendMessage?chat_id = 12345 & text = Hello