from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=100)
    code = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'name')
