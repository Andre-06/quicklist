from django.http import JsonResponse
from django.shortcuts import render
from .models import Tarefas
from django.contrib import messages
from django.contrib.messages import constants

def lists(request):
    lista = Tarefas.objects.all
    
    if request.method == 'GET':
        return render(request, 'checklist.html', {'user': request.user, 'lista':lista})
    elif request.method == 'POST':
        descricao = request.POST.get('descricao')
        
        if len(descricao) == 0:
            messages.add_message(request, constants.WARNING, 'Preencha o campo corretamente')
            return render(request, 'checklist.html', {'user': request.user, 'lista':lista})
        
        try:    
            tarefa = Tarefas(
                descricao= descricao,
                usuario_id= request.user
            )

            tarefa.save()
            
            lista = Tarefas.objects.filter(usuario_id=request.user)
            return render(request, 'checklist.html', {'user': request.user, 'lista':lista})
        except:
            messages.add_message(request, constants.ERROR, 'Ocorreu um erro inesperado, tente novamente mais tarde X_X')
            return render(request, 'checklist.html', {'user': request.user, 'lista':lista})

def update_task(request, id_tarefa):
    try:
        tarefa = Tarefas.objects.get(id=id_tarefa)
        tarefa.concluida = request.request.POST.get('concluida') == 'true'
        tarefa.save()
        return JsonResponse({'status': 'OK'})
    except:
        return
