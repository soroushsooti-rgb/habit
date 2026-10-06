
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
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    event_date = models.DateTimeField()
    days = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name='habit_unique'),
        ]

    def __str__(self):
        return self.name


class Cheking (models.Model):
    habit = models.ForeignKey(
        Habits, on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['habit'], name='cheking_unique'),
        ]

    def __str__(self):
        return self.habit.name
