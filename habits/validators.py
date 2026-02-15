from rest_framework.serializers import ValidationError

from django.core.exceptions import ValidationError

def validate_habit(habit):
    """
    Валидирует экземпляр модели Habit по следующим правилам:
    1. Нельзя одновременно заполнять related_habit и award.
    2. duration не может превышать 120 секунд.
    3. related_habit может ссылаться только на приятную привычку (is_pleasant=True).
    4. Приятная привычка (is_pleasant=True) не может иметь award или related_habit.
    5. periodicity должна быть в диапазоне от 1 до 7 дней (включительно).
    """
    errors = {}

    # 1. Конфликт related_habit и award
    if habit.related_habit and habit.award:
        msg = "Нельзя одновременно указывать связанную привычку и вознаграждение."
        errors.setdefault('related_habit', []).append(msg)
        errors.setdefault('award', []).append(msg)

    # 2. Длительность выполнения
    if habit.duration is not None and habit.duration > 120:
        errors.setdefault('duration', []).append(
            "Время выполнения не должно превышать 120 секунд."
        )

    # 3. Связанная привычка должна быть приятной
    if habit.related_habit and not habit.related_habit.is_pleasant:
        errors.setdefault('related_habit', []).append(
            "Связанная привычка может быть только приятной (is_pleasant=True)."
        )

    # 4. Приятная привычка не может иметь вознаграждение или связанную привычку
    if habit.is_pleasant:
        if habit.award:
            errors.setdefault('award', []).append(
                "У приятной привычки не может быть вознаграждения."
            )
        if habit.related_habit:
            errors.setdefault('related_habit', []).append(
                "У приятной привычки не может быть связанной привычки."
            )

    # 5. Периодичность (1-7 дней)
    if habit.periodicity is None:
        errors.setdefault('periodicity', []).append(
            "Периодичность должна быть указана."
        )
    elif not (1 <= habit.periodicity <= 7):
        errors.setdefault('periodicity', []).append(
            "Периодичность должна быть от 1 до 7 дней (нельзя реже 1 раза в неделю)."
        )

    if errors:
        raise ValidationError(errors)

