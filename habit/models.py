from django.conf import settings
from django.db import models
from django.utils import timezone


DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


class Habit(models.Model):
    class Frequency(models.TextChoices):
        DAILY = 'DAILY', 'روزانه'
        WEEKLY = 'WEEKLY', 'هفتگی'
        MONTHLY = 'MONTHLY', 'ماهانه'

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    frequency = models.CharField(
        max_length=10,
        choices=Frequency.choices,
        default=Frequency.DAILY,
        verbose_name='loop'
    )
    day_of_week = models.PositiveSmallIntegerField(
        choices=DAYS_OF_WEEK,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'name')]
        ordering = ['user', 'frequency']

    def __str__(self):
        return f"{self.name} ({self.get_frequency_display()})"


class HabitCheck(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='checkings'
    )

    checked_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = [('habit')]
        ordering = ['-checked_date']

    def __str__(self):
        return f"{self.habit.name} - {self.checked_date}"
