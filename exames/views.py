from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TiposExames, PedidosExames, SolicitacaoExame
from datetime import datetime
# Create your views here.

@login_required
def solicitar_exames(request):
    tipos_exames = TiposExames.objects.all()
    if request.method == 'GET':
        print(tipos_exames)
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames})
    elif request.method == 'POST':
        exames_id = request.POST.getlist('exames')
        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)

        preco_total = 0
        data = datetime.now()
        for i in solicitacao_exames:
            if i.disponivel == True:
                preco_total += i.preco
        print(preco_total)

        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames, 
                                                         'solicitacao_exames': solicitacao_exames,
                                                         'preco_total': preco_total,
                                                         'data': data})
    
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    solicitacao_exames = TiposExames.objects.filter(id__in = exames_id)
    pedido_exame = PedidosExames(
        usuario = request.user,
        data = datetime.now()
    )
    pedido_exame.save()

    for exame in solicitacao_exames:
        solicitacao_exames_temp = SolicitacaoExame(
            usuario = request.user,
            exame = exame,
            status= "E"
        )
        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)

    pedido_exame.save()

    return HttpResponse('url funciona')