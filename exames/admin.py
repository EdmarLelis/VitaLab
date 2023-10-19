from django.contrib import admin
from .models import TiposExames, SolicitacaoExame

# Register your models here.
admin.site.register(TiposExames)
admin.site.register(SolicitacaoExame)