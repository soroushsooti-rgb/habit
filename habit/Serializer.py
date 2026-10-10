from rest_framework import serializers
from .models import Habit, HabitCheck


class HabitSerializers (serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'user', 'date', 'day_of_week', 'frequency',
                  'day_of_week', 'day_of_month', 'reminder_time', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ChekingSerializers (serializers.ModelSerializer):
    model = HabitCheck
    fields = ['id', 'name', 'checked_date']
