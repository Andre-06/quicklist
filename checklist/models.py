from django.db import models
from users.models import User

class Tarefas(models.Model):
    descricao = models.CharField(max_length=280)
    concluida = models.BooleanField(default=False)
    usuario_id = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.descricao

# Create your models here.
