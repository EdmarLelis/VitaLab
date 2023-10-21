from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TiposExames, PedidosExames, SolicitacaoExame
from datetime import datetime
from django.contrib.messages import constants
from django.contrib import messages
# Create your views here.

@login_required
def solicitar_exames(request):
    tipos_exames = TiposExames.objects.all()
    if request.method == 'GET':
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames})
    elif request.method == 'POST':
        exames_id = request.POST.getlist('exames')
        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)

        preco_total = 0
        data = datetime.now()
        for i in solicitacao_exames:
            if i.disponivel == True:
                preco_total += i.preco

        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames, 
                                                         'solicitacao_exames': solicitacao_exames,
                                                         'preco_total': preco_total,
                                                         'data': data})

@login_required 
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    solicitacao_exames = TiposExames.objects.filter(id__in = exames_id)
    valido = True
    for exame in solicitacao_exames:
        if exame.disponivel == False:
            valido = False
    
    pedido_exame = PedidosExames(
        usuario = request.user,
        data = datetime.now()
    )

    if valido == True:
        pedido_exame.save()

    if valido == True:
        for exame in solicitacao_exames:
            if exame.disponivel == True:
                solicitacao_exames_temp = SolicitacaoExame(
                    usuario = request.user,
                    exame = exame,
                    status= "E"
                )
            solicitacao_exames_temp.save()
            pedido_exame.exames.add(solicitacao_exames_temp)

        pedido_exame.save()
        messages.add_message(request, constants.SUCCESS, 'Pedido de exames realizado com sucesso!')
    
    else:
        messages.add_message(request, constants.ERROR, 'Pedido negado, um ou mais exames solicitados estão indisponíveis.')

    valido = False
    return redirect('/exames/gerenciar_pedidos')

@login_required
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames': pedidos_exames})

def cancelar_pedido(request, pedido_id):
    pedido = PedidosExames.objects.get(id=pedido_id)
    if pedido.usuario == request.user:
        pedido.agendado = False
        pedido.save()
    else:
        messages.add_message(request, constants.ERROR, f'Você não pode cancelar o pedido de ID {pedido_id}, ele não é seu!')
    return redirect('/exames/gerenciar_pedidos')