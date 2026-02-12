from rest_framework import serializers

from habits.models import Place, Award, Habit


class PlaceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class AwardSerializers(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'

class HabitSerializers(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'