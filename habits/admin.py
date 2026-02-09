from django.contrib import admin

from habits.models import Habit, Place, Award

admin.site.register(Habit)
admin.site.register(Place)
admin.site.register(Award)
