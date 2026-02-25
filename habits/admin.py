from django.contrib import admin

from habits.models import Award, Habit, Place

admin.site.register(Habit)
admin.site.register(Place)
admin.site.register(Award)
