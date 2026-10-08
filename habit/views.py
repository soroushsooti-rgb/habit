from django.shortcuts import render
from rest_framework import viewsets
from .models import Habit, HabitCheck
from .Serializer import ChekingSerializers, HabitSerializers


class HabitViewSet (viewsets.ModelViewSet):
    serializer_class = HabitSerializers

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChekingViewSet(viewsets.ModelViewSet):
    serializer_class = ChekingSerializers

    def get_queryset(self):
        return HabitCheck.objects.filter(habit__user=self.request.user)
