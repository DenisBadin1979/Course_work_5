from django.core.serializers import serialize
from django.shortcuts import render
from mypyc.primitives.exc_ops import raise_exception_op
from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from habits.models import Place, Award, Habit
from habits.pagination import HabitPagination
from habits.permissions import IsOwnerOrPublicReadOnly
from habits.serializers import PlaceSerializers, AwardSerializers, HabitSerializers


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

class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    pagination_class = HabitPagination
    permission_classes = [IsOwnerOrPublicReadOnly]  # проверка прав на уровне запроса

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Авторизованный пользователь видит свои привычки и все публичные
            return Habit.objects.filter(is_public=True) | Habit.objects.filter(user=user)
        else:
            # Анонимный пользователь видит только публичные
            return Habit.objects.filter(is_public=True)

class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrPublicReadOnly]

class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrPublicReadOnly]

class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrPublicReadOnly]

class HabitDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrPublicReadOnly]