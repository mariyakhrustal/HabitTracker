from rest_framework.serializers import ModelSerializer, ValidationError

from habits.models import Habit
from habits.validators import DurationValidator, PeriodicityValidator


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)
        validators = [
            DurationValidator(field="duration"),
            PeriodicityValidator(field="periodicity"),
        ]

    def validate(self, data):
        reward = data.get("reward")
        related_habit = data.get("related_habit")
        is_pleasant = data.get("is_pleasant")

        if reward and related_habit:
            raise ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")
        if is_pleasant and reward:
            raise ValidationError("У приятной привычки не может быть вознаграждения.")
        if is_pleasant and related_habit:
            raise ValidationError("У приятной привычки не может быть связанной привычки.")
        if related_habit and not is_pleasant:
            raise ValidationError("В связанные привычки могут попадать только приятные привычки.")
        return data
