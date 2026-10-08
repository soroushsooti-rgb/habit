from django.contrib import admin
from .models import Habit, HabitCheck

admin.site.register(Habit)
admin.site.register(HabitCheck)
