from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com", password="1234")
        self.other_user = User.objects.create(email="other@test.com", password="1234")

        self.habit1 = Habit.objects.create(
            user=self.user,
            action="Утренняя зарядка",
            place="Дом",
            time="08:00:00",
            duration=60,
            is_public=False,
        )
        self.habit2 = Habit.objects.create(
            user=self.user,
            action="Прогулка",
            place="Парк",
            time="19:00:00",
            duration=120,
            is_public=True,
        )
        self.habit3 = Habit.objects.create(
            user=self.other_user,
            action="Чтение книги",
            place="Дом",
            time="21:00:00",
            duration=60,
            is_public=True,
        )

    def test_habit_list_current_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_habit_create_forbidden_anonymous(self):
        url = reverse("habits:habit-list")
        data = {"action": "Новая привычка", "place": "Офис", "time": "10:00:00", "duration": 90}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_habit_create(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-list")
        data = {"action": "Новая привычка", "place": "Офис", "time": "10:00:00", "duration": 90}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.filter(user=self.user).count(), 3)

    def test_habit_update_owner(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-detail", args=(self.habit1.pk,))
        data = {"action": "Обновленная зарядка"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit1.refresh_from_db()
        self.assertEqual(self.habit1.action, "Обновленная зарядка")

    def test_habit_delete_owner(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-detail", args=(self.habit1.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.habit1.pk).exists())

    def test_habit_update_not_owner_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-detail", args=(self.habit3.pk,))
        data = {"action": "Попытка обновления"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_habit_delete_not_owner_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-detail", args=(self.habit3.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_habit_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:public-habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
