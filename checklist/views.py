from django.http import JsonResponse
from django.shortcuts import render
from .models import Task
from django.contrib import messages
from django.contrib.messages import constants


def lists(request):
    task_list = Task.objects.all

    print(request.user)
    print('name:' + request.user.name)

    if request.method == 'GET':
        return render(request, 'checklist.html', {'user': request.user, 'list': task_list})
    elif request.method == 'POST':
        description = request.POST.get('description')

        if len(description) == 0:
            messages.add_message(request, constants.WARNING, 'Preencha o campo corretamente')
            return render(request, 'checklist.html', {'user': request.user, 'list': task_list})

        try:
            task = Task(
                description=description,
                id_user=request.user
            )

            task.save()

            task_list = Task.objects.filter(id_user=request.user)
            return render(request, 'checklist.html', {'user': request.user, 'list': task_list})
        except:
            messages.add_message(request, constants.ERROR, 'Ocorreu um erro inesperado, tente novamente mais tarde X_X')
            return render(request, 'checklist.html', {'user': request.user, 'list': task_list})


def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.checked = request.request.POST.get('checked') == 'true'
        task.save()
        return JsonResponse({'status': 'OK'})
    except:
        return
