from typing import Any
from django.db import models

# Create your models here.
class TiposExames(models.Model):
    tipo_choices = (
        ('I', 'Exame de Imagem'),
        ('S', 'Exame de Sangue')
    )
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=1, choices=tipo_choices)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    horario_inicial = models.IntegerField()
    horario_final = models.IntegerField()

    def __str__(self):
        return self.nome