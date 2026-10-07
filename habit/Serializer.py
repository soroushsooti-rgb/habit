from rest_framework import serializers
from .models import Habits, Cheking


class HabitSerializers (serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = ['id', 'name', 'user', 'date', 'day_of_week']
        read_only_fields = ['user']


class ChekingSerializers (serializers.ModelSerializer):
    model = Cheking
    fields = ['name', 'id']
