from rest_framework import serializers
from .models import Habits, Cheking


class habitserializers (serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = ['id', 'name', 'user', 'date', 'day_of_week']
        read_only_fields = ['user']


class chekingserializers (serializers.ModelSerializer):
    model = Cheking
    fields = ['name', 'id']
