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
        """
        Валидация, учитывающая все правила модели.
        """
        # Получаем текущий экземпляр, если он есть (при частичном обновлении)
        instance = self.instance

        # Собираем полные данные для проверки: берём текущие значения из instance
        # и обновляем их переданными в attrs
        full_data = {}
        if instance:
            # Для каждого поля модели берём значение из instance,
            # но если оно есть в attrs, используем attrs
            for field in self.Meta.model._meta.get_fields():
                if field.name in attrs:
                    full_data[field.name] = attrs[field.name]
                elif hasattr(instance, field.name):
                    full_data[field.name] = getattr(instance, field.name)
        else:
            # Создание нового объекта — используем только attrs
            full_data = attrs

        # Создаём временный объект модели для передачи в валидатор
        # (это не сохраняет его в БД)
        temp_habit = Habit(**full_data)

        # Вызываем наш валидатор
        # Валидатор выбросит ValidationError, который DRF преобразует в нужный ответ
        validate_habit(temp_habit)

        return attrs
