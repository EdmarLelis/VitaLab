from typing import Any
from django.db import models
from django.contrib.auth.models import User

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
    

class SolicitacaoExame(models.Model):
    choice_status = (
        ('E', 'Em análise'),
        ('F', 'Finalisado')
    )
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exame = models.ForeignKey(TiposExames, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=choice_status)
    resultado = models.FileField(upload_to="resultados", null=True, blank=True)
    requer_senha = models.BooleanField(default=False)
    senha = models.CharField(max_length=16, null=True, blank=True)