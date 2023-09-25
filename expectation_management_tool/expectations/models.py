from django.db import models
from core.models import User


class ManagingExpectation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expected_role = models.CharField(max_length=255)
    expected_finished_time = models.DateTimeField()
    is_archive = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            managing_expectation = ManagingExpectation.objects.filter(user=self.user)
            managing_expectation.update(is_archive=True)
        super().save(*args, **kwargs)