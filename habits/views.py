from django.shortcuts import render
from rest_framework import viewsets

from habits.models import Place
from habits.serializers import PlaceSerializers


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializers
    queryset = Place.objects.all()


