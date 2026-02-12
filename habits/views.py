from django.core.serializers import serialize
from django.shortcuts import render
from mypyc.primitives.exc_ops import raise_exception_op
from rest_framework import viewsets, status
from rest_framework.response import Response

from habits.models import Place, Award
from habits.serializers import PlaceSerializers, AwardSerializers


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializers
    queryset = Place.objects.all()

    def create (self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid (raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response (serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

class AwardViewSet(viewsets.ModelViewSet):
    serializer_class = AwardSerializers
    queryset = Award.objects.all()

    def create (self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid (raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response (serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()


