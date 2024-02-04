from django.db import models
from users.models import User


class Task(models.Model):
    description = models.CharField(max_length=280)
    checked = models.BooleanField(default=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

# Create your models here.
