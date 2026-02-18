from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status, generics
from rest_framework.test import APITestCase
from habits.models import Habit, Place, Award
from habits.permissions import IsOwnerOrPublicReadOnly
from habits.serializers import HabitSerializers
from habits.validators import validate_habit
from rest_framework.exceptions import ValidationError

User = get_user_model()


class PlaceViewSetTests(APITestCase):
    """Тесты для модели Place и ViewSet (с namespace)"""

    def setUp(self):
        self.place_data = {
            "location": "Дом",
            "clarifying": "В гостиной на коврике"
        }
        self.place = Place.objects.create(**self.place_data)
        self.list_url = reverse("habits:places-list")
        self.detail_url = reverse("habits:places-detail", args=[self.place.pk])

    def test_list_places(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_place(self):
        new_data = {
            "location": "Улица",
            "clarifying": "Парк"
        }
        response = self.client.post(self.list_url, new_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 2)
        self.assertEqual(Place.objects.get(location="Улица").clarifying, "Парк")

    def test_create_many_places(self):
        data = [
            {"location": "Работа", "clarifying": "Офис"},
            {"location": "Спортзал", "clarifying": "Тренажёрный зал"}
        ]
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 3)

    def test_retrieve_place(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["location"], self.place.location)

    def test_update_place(self):
        updated_data = {"location": "Дом", "clarifying": "На кухне"}
        response = self.client.put(self.detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.place.refresh_from_db()
        self.assertEqual(self.place.clarifying, "На кухне")

    def test_delete_place(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Place.objects.count(), 0)


class AwardViewSetTests(APITestCase):
    """Тесты для модели Award и ViewSet (с namespace)"""

    def setUp(self):
        self.award_data = {
            "award": "Шоколадка",
            "description": "Съесть кусочек тёмного шоколада"
        }
        self.award = Award.objects.create(**self.award_data)
        self.list_url = reverse("habits:awards-list")
        self.detail_url = reverse("habits:awards-detail", args=[self.award.pk])

    def test_list_awards(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_award(self):
        new_data = {
            "award": "Кофе",
            "description": "Выпить чашечку ароматного кофе"
        }
        response = self.client.post(self.list_url, new_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Award.objects.count(), 2)

    def test_create_many_awards(self):
        data = [
            {"award": "Прогулка", "description": "Выйти на улицу на 15 минут"},
            {"award": "Книга", "description": "Почитать любимую книгу"}
        ]
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Award.objects.count(), 3)

    def test_retrieve_award(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["award"], self.award.award)

    def test_update_award(self):
        updated_data = {"award": "Шоколадка", "description": "Съесть молочный шоколад"}
        response = self.client.put(self.detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.award.refresh_from_db()
        self.assertEqual(self.award.description, "Съесть молочный шоколад")

    def test_delete_award(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Award.objects.count(), 0)


class HabitValidatorTests(APITestCase):
    """Прямые тесты валидатора модели Habit (без изменения)"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.place = Place.objects.create(location="Дом", clarifying="Комната")
        self.award = Award.objects.create(award="Чай", description="Выпить чаю")
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            action="Послушать музыку",
            is_pleasant=True,
            periodicity=3,
            duration=60
        )

    def test_conflict_related_and_award(self):
        habit = Habit(
            user=self.user,
            action="Сделать зарядку",
            related_habit=self.pleasant_habit,
            award=self.award,
            periodicity=5,
            duration=100
        )
        with self.assertRaises(ValidationError) as context:
            validate_habit(habit)
        errors = context.exception.detail
        self.assertIn("related_habit", errors)
        self.assertIn("award", errors)
        self.assertIn("Нельзя одновременно указывать", str(errors))

    def test_duration_exceeds_120(self):
        habit = Habit(
            user=self.user,
            action="Пробежка",
            duration=150,
            periodicity=2
        )
        with self.assertRaises(ValidationError) as context:
            validate_habit(habit)
        self.assertIn("duration", context.exception.detail)

    def test_related_habit_not_pleasant(self):
        non_pleasant = Habit.objects.create(
            user=self.user,
            action="Уборка",
            is_pleasant=False,
            periodicity=1
        )
        habit = Habit(
            user=self.user,
            action="Полезная привычка",
            related_habit=non_pleasant,
            periodicity=3
        )
        with self.assertRaises(ValidationError) as context:
            validate_habit(habit)
        self.assertIn("related_habit", context.exception.detail)

    def test_pleasant_habit_with_award(self):
        habit = Habit(
            user=self.user,
            action="Приятная",
            is_pleasant=True,
            award=self.award,
            periodicity=4
        )
        with self.assertRaises(ValidationError) as context:
            validate_habit(habit)
        self.assertIn("award", context.exception.detail)

    def test_pleasant_habit_with_related(self):
        habit = Habit(
            user=self.user,
            action="Приятная",
            is_pleasant=True,
            related_habit=self.pleasant_habit,
            periodicity=4
        )
        with self.assertRaises(ValidationError) as context:
            validate_habit(habit)
        self.assertIn("related_habit", context.exception.detail)

    def test_periodicity_out_of_range(self):
        habit = Habit(
            user=self.user,
            action="Тест",
            periodicity=8,
            duration=30
        )
        with self.assertRaises(ValidationError) as context:
            validate_habit(habit)
        self.assertIn("periodicity", context.exception.detail)

        habit.periodicity = 0
        with self.assertRaises(ValidationError) as context:
            validate_habit(habit)
        self.assertIn("periodicity", context.exception.detail)

    def test_periodicity_none(self):
        habit = Habit(
            user=self.user,
            action="Тест",
            periodicity=None,
            duration=30
        )
        with self.assertRaises(ValidationError) as context:
            validate_habit(habit)
        self.assertIn("periodicity", context.exception.detail)

    def test_valid_habit(self):
        habit = Habit(
            user=self.user,
            action="Читать книгу",
            place=self.place,
            related_habit=self.pleasant_habit,
            periodicity=5,
            duration=100
        )
        try:
            validate_habit(habit)
        except ValidationError:
            self.fail("validate_habit raised ValidationError for valid habit")


class HabitAPITests(APITestCase):
    """Тесты для CRUD привычек через API с учётом реальных маршрутов и namespace"""

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")
        self.place = Place.objects.create(location="Парк", clarifying="Скамейка")
        self.award = Award.objects.create(award="Мороженое", description="Съесть мороженое")
        self.pleasant = Habit.objects.create(
            user=self.user1,
            action="Смотреть на закат",
            is_pleasant=True,
            periodicity=2,
            duration=60
        )

        self.public_habit = Habit.objects.create(
            user=self.user1,
            action="Пробежка",
            place=self.place,
            is_public=True,
            periodicity=3,
            duration=60
        )
        self.private_habit = Habit.objects.create(
            user=self.user1,
            action="Медитация",
            place=self.place,
            is_public=False,
            periodicity=1,
            duration=100
        )
        self.other_habit = Habit.objects.create(
            user=self.user2,
            action="Плавание",
            place=self.place,
            is_public=False,
            periodicity=2,
            duration=90
        )

        # URL'ы согласно habits/urls.py
        self.list_url = reverse("habits:habit-list")
        self.create_url = reverse("habits:habit-create")
        self.retrieve_url_public = reverse("habits:habit-retrieve", args=[self.public_habit.pk])
        self.retrieve_url_private = reverse("habits:habit-retrieve", args=[self.private_habit.pk])
        self.retrieve_url_other = reverse("habits:habit-retrieve", args=[self.other_habit.pk])
        self.update_url_private = reverse("habits:habit-update", args=[self.private_habit.pk])
        self.delete_url_private = reverse("habits:habit-delete", args=[self.private_habit.pk])

    # ---------- Тесты на получение списка ----------
    def test_list_habits_anonymous(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if "results" in response.data:
            results = response.data["results"]
        else:
            results = response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["action"], self.public_habit.action)

    def test_list_habits_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)
        if "results" in response.data:
            results = response.data["results"]
        else:
            results = response.data
        self.assertEqual(len(results), 3)  # user1 имеет 3 привычки
        actions = {h["action"] for h in results}
        self.assertIn(self.public_habit.action, actions)
        self.assertIn(self.private_habit.action, actions)
        self.assertIn(self.pleasant.action, actions)

    # ---------- Тесты на получение одной привычки ----------
    def test_retrieve_own_habit(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.retrieve_url_private)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], self.private_habit.action)

    def test_retrieve_public_habit_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.retrieve_url_public)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], self.public_habit.action)

    def test_retrieve_private_habit_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.retrieve_url_private)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_anonymous_public(self):
        response = self.client.get(self.retrieve_url_public)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_retrieve_anonymous_private(self):
    #     response = self.client.get(self.retrieve_url_private)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------- Тесты на создание ----------
    # def test_create_habit_authenticated(self):
    #     self.client.force_authenticate(user=self.user1)
    #     data = {
    #         "action": "Новая привычка",
    #         "place": self.place.pk,
    #         "related_habit": self.pleasant.pk,
    #         "periodicity": 4,
    #         "duration": 90,
    #         "time": "08:00:00"
    #     }
    #     response = self.client.post(self.create_url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Habit.objects.count(), 5)  # было 4, стало 5
    #     new_habit = Habit.objects.get(action="Новая привычка")
    #     self.assertEqual(new_habit.user, self.user1)


    def test_create_habit_unauthenticated(self):
        data = {"action": "Новая привычка", "periodicity": 4, "duration": 90}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_habit_validation_error(self):
        self.client.force_authenticate(user=self.user1)
        data = {"action": "Плохая привычка", "duration": 150, "periodicity": 3}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("duration", response.data)

    # ---------- Тесты на обновление ----------
    def test_update_own_habit(self):
        self.client.force_authenticate(user=self.user1)
        data = {"action": "Обновлённая привычка"}
        response = self.client.patch(self.update_url_private, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.private_habit.refresh_from_db()
        self.assertEqual(self.private_habit.action, "Обновлённая привычка")

    def test_update_not_own_habit(self):
        self.client.force_authenticate(user=self.user2)
        data = {"action": "Попытка взлома"}
        response = self.client.patch(self.update_url_private, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------- Тесты на удаление ----------
    def test_delete_own_habit(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.delete_url_private)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.private_habit.pk).exists())

    def test_delete_not_own_habit(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.delete_url_private)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------- Тест пагинации ----------
    def test_pagination(self):
        for i in range(15):
            Habit.objects.create(
                user=self.user1,
                action=f"Привычка {i}",
                is_public=True,
                periodicity=1,
                duration=30
            )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertEqual(response.data["count"], Habit.objects.filter(is_public=True).count())
        self.assertLessEqual(len(response.data["results"]), 10)

class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrPublicReadOnly]

    def perform_create(self, serializer):
        print(f"Сохранение с пользователем: {self.request.user}")
        serializer.save(user=self.request.user)
