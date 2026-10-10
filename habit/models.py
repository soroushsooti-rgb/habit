from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

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
        DAILY = 'DAILY'
        WEEKLY = 'WEEKLY'
        MONTHLY = 'MONTHLY'

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
    day_of_month = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    reminder_time = models.TimeField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Habit Tracking Conditions

    def clean(self):
        super().clean()
        if self.frequency == self.Frequency.DAILY:
            if not self.reminder_time:
                raise ValidationError(
                    'You must specify a time for daily habits.')
            self.day_of_week = None
            self.day_of_month = None

        elif self.frequency == self.Frequency.WEEKLY:

            if self.day_of_week is None:
                raise ValidationError(
                    'You must select a day of the week for weekly habits.')
            self.reminder_time = None
            self.day_of_month = None

        elif self.frequency == self.Frequency.MONTHLY:
            if not self.day_of_month:
                raise ValidationError(
                    'You must specify a day of the month for monthly habits.')
            if not (1 <= self.day_of_month <= 31):
                raise ValidationError(
                    'The day of the month must be between 1 and 31.')
            self.reminder_time = None
            self.day_of_week = None

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:

        unique_together = [('user', 'name')]
        indexes = [
            models.Index(fields=['user', 'name'],
                         name='idx_habit_habit_date'),
        ]
        ordering = ['user', 'frequency']

    def __str__(self):
        return f"{self.name}"


class HabitCheck(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='checkings'
    )
    checked_date = models.DateField(default=timezone.now)

    def clean(self):

        super().clean()

        if not hasattr(self, 'habit'):
            return

        if self.habit.frequency == Habit.Frequency.WEEKLY:
            if self.checked_date.weekday() != self.habit.day_of_week:
                raise ValidationError(
                    'This habit can only be checked on the selected day of the week.')

        elif self.habit.frequency == Habit.Frequency.MONTHLY:
            if self.checked_date.day != self.habit.day_of_month:
                raise ValidationError(
                    'This habit can only be checked on the selected day of the month.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = [('habit', 'checked_date')]
        indexes = [
            models.Index(fields=['habit', 'checked_date'],
                         name='idx_habit_checked_date'),
        ]
        ordering = ['-checked_date']

    def __str__(self):
        return f"{self.habit.name} - {self.checked_date}"
