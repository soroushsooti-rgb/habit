from django.shortcuts import render
from rest_framework import viewsets
from .Serializer import chekingserializers,habitserializers

class habitciewset (viewsets.ModelViewSet):
    serializer_class = habitserializers

