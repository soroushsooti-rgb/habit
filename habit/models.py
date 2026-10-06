
# from django.conf import settings
# from django.db import models



# DAYS_OF_WEEK = (
#     (0, 'Monday'),
#     (1, 'Tuesday'),
#     (2, 'Wednesday'),
#     (3, 'Thursday'),
#     (4, 'Friday'),
#     (5, 'Saturday'),
#     (6, 'Sunday'),
# )


# class Habits (models.Model):
#     name = models.CharField(max_length=255)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#     event_date = models.DateTimeField()

#     def __str__(self):
#         return self.name


# class Cheking (models.Model):
#     habit = models.ForeignKey(
#         Habits, on_delete=models.CASCADE,
#         related_name="checkins"
#     )
#     days = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK, default=0)

#     def __str__(self):
#         return f"{self.habit.name} - {self.get_days_display()}"


# # class days_in_month (models.Model):
# #     name = models.CharField(max_length=20, blank=True)
# #     month = models.DateField(help_text="days in month")

# #     def __str__(self):
# #         return f"{self.name} - {str(self.month)}"
from django.conf import settings
from django.db import models
from django.utils import timezone

DAYS_OF_WEEK = (
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday"),
)


class Habits(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    event_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Cheking(models.Model):
    habit = models.ForeignKey(
        Habits, on_delete=models.CASCADE, related_name="checkins"
    )
    days = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK, default=0)

    def __str__(self):
        # جلوگیری قطعی از خطای ۵۰۰
        habit_name = self.habit.name if self.habit_id else "No Habit"
        return f"{habit_name} - {self.get_days_display()}"
