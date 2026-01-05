from rest_framework.serializers import ValidationError


class DurationValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        duration = value.get(self.field)
        if duration is None:
            return duration
        if duration > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")


class PeriodicityValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodicity = value.get(self.field)
        if periodicity is None:
            periodicity = 1
        if periodicity < 1 or periodicity > 7:
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")
