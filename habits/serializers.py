from rest_framework import serializers

from habits.models import Award, Habit, Place
from habits.validators import validate_habit


class PlaceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"


class AwardSerializers(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = "__all__"


class HabitSerializers(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, attrs):
        instance = self.instance

        if instance:
            full_data = {}
            # Берём только прямые поля модели
            for field in instance._meta.fields:
                if field.name in attrs:
                    full_data[field.name] = attrs[field.name]
                else:
                    full_data[field.name] = getattr(instance, field.name)
        else:
            full_data = attrs

        temp_habit = Habit(**full_data)
        validate_habit(temp_habit)
        return attrs
