from django.shortcuts import render
from .models import Tarefas

def lists(request):
    if request.method == 'GET':
        lista = Tarefas.objects.filter(usuario_id=request.user)
        return render(request, 'checklist.html', {'user': request.user, 'lista':lista})