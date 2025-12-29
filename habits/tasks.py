from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_tg_reminder


@shared_task
def remind_tg_habit():
    now = timezone.localtime()
    current_hour = now.hour
    current_minute = now.minute
    habits = Habit.objects.filter(
        user__telegram_id__isnull=False,
        time__hour=current_hour,
        time__minute=current_minute,
    )
    for habit in habits:
        if habit.last_reminded:
            delta_days = (now.date() - habit.last_reminded.date()).days
            if delta_days < habit.periodicity:
                continue
        reward_text = ""
        if habit.reward:
            reward_text = f"Награда: {habit.reward}"
        elif habit.related_habit:
            reward_text = f"Затем можно: {habit.related_habit.action}"
        message = f"Пора {habit.action} в {habit.place}! {reward_text}"
        send_tg_reminder(habit.user.telegram_id, message)
        habit.last_reminded = now
        habit.save(update_fields=["last_reminded"])
