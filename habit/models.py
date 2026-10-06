from django.db import models

# Create your models here.
# from django.conf import settings
# from django.core.exceptions import ValidationError
# from django.db import models


# class WeekDay(models.Model):

#     code = models.CharField(
#         max_length=3, unique=True)
#     name = models.CharField(max_length=20)
#     order = models.PositiveSmallIntegerField(unique=True)

#     class Meta:
#         ordering = ["order"]

#     def __str__(self):
#         return self.name


# class Habit(models.Model):
#     class Frequency(models.TextChoices):
#         DAILY = "daily", "Daily"
#         WEEKLY = "weekly", "Weekly"
#         MONTHLY = "monthly", "Monthly"

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="habits",
#     )
#     name = models.CharField(max_length=255)
#     frequency = models.CharField(
#         max_length=20,
#         choices=Frequency.choices,
#         default=Frequency.DAILY,
#     )

#     days_for_week = models.ManyToManyField(
#         WeekDay,
#         blank=True,
#         related_name="habits",
#     )
#     start_date = models.DateField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} ({self.user})"


# class CheckIn(models.Model):
#     habit = models.ForeignKey(
#         Habit,
#         on_delete=models.CASCADE,
#         related_name="checkins",
#     )
#     date = models.DateField()
#     is_completed = models.BooleanField(default=True)
#     completed_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["habit", "date"],
#                 name="unique_habit_checkin_per_day",
#             )
#         ]

#     def __str__(self):
#         status = "Completed" if self.is_completed else "Missed"
#         return f"{self.habit.name} - {self.date} - {status}"

# from django.conf import settings
# from django.db import models
# from datetime import date

# DAILY = 'daily'
# WEEKLY = 'weekly'
# MONTHLY = 'monthly'

# mods = [
#     (DAILY, 'dayli '),
#     (WEEKLY, 'weekly'),
#     (MONTHLY, 'monthly'),
# ]


# class Habits (models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="habit",
#     )

#     name = models.CharField(
#         max_length=255
#     )
#     mode = models.CharField(
#         max_length=20,
#         choices=mods,
#         default=DAILY
#     )

#     days_of_week = models.JSONField(
#         default=list,
#         blank=True,
#         verbose_name='ays_of_week'
#     )
#     days_of_month = models.JSONField(
#         default=list,
#         blank=True,
#         verbose_name='days_of_month '
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name='created_at'
#     )


# class Checking(models.Model):
#     habit = models.ForeignKey(
#         Habits,
#         on_delete=models.CASCADE,
#         related_name="checkings",
#     )
#     date = models.DateField(default=date.today)
#     is_done = models.BooleanField(default=False)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["habit", "date"],
#                 name="unique_habit_checking_per_day",
#             )
#         ]

#     def __str__(self):
#         return f"{self.habit.name} - {self.date} - {self.is_done}"

from django.conf import settings
from django.db import models



DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


class Habits (models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    event_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Cheking (models.Model):
    habit = models.ForeignKey(
        Habits, on_delete=models.CASCADE,
        related_name="checkins"
    )
    days = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)

    def __str__(self):
        return f"{self.habit.name} - {self.get_days_display()}"


class days_in_month (models.Model):
    name = models.CharField(max_length=20, blank=True)
    month = models.DateField(help_text="days in month")

    def __str__(self):
        return f"{self.name} - {str(self.month)}"
