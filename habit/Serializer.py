from rest_framework import serializers
from .models import Habit, HabitCheck


class HabitSerializers (serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['name', 'user', 'date', 'day_of_week', 'frequency']
        read_only_fields = ['user']


class ChekingSerializers (serializers.ModelSerializer):
    model = HabitCheck
    fields = ['name', 'checked_date']
