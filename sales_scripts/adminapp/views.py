from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.models import ScriptsUser, UserRights
from adminapp.models import Script, ControlTop, ControlToControl, Situation
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import random, string

# Create your views here.

# Список скриптов получить
# Создать скрипт
# Редактировать скрипт
# Удалить скрипт

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

@login_required(login_url='/auth/login/')
def no_rights(request):
    title = 'Попытка проникновения! Тревога!'
    container_size = 'small_container'

    content = {
        'title': title,
        'container_size': container_size

    }

    return render(request, 'adminapp/no_rights.html', content)

@login_required(login_url='/auth/login/')
def control_post(request):
    title = 'пункт управления'
    container_size = 'large_container'
    scripts = Script.objects.filter(user__pk=request.user.pk).order_by('last_modified')
    rights = get_object_or_404(UserRights, user__pk=request.user.pk)


    content = {
        'title': title,
        'scripts': scripts,
        'rights': rights,
        'container_size': container_size
    }

    return render(request, 'adminapp/control_post.html', content)

@login_required(login_url='/auth/login/')
def team_view(request):
    title = 'Палуба/команда построена'

    rights = get_object_or_404(UserRights, user__pk=request.user.pk)

    if not rights.can_edit_users:
        return HttpResponseRedirect(reverse('admin:no_rights'))


    content = {
        'title': title
    }

    return render(request, 'adminapp/team_view.html', content)


@login_required(login_url='/auth/login/')
def scripts_read(request):
    title = 'админка/скрипты'

    scripts_list = Script.objects.filter(user__username=request.user.username).order_by('-last_modified')

    content = {
        'title': title,
        'scripts_list': scripts_list
    }

    return render(request, 'adminapp/scripts_read.html', content)

@login_required(login_url='/auth/login/')
def script_create(request):
    title = 'новый скрипт'

    if request.method == 'POST':
        new_script = Script(user=request.user, name=request.POST['script_name'], url=request.POST['url'])
        new_script.save()
        return HttpResponseRedirect(reverse('admin:scripts_read'))

    unique_url = randomword(16)

    content = {
        'title': title,
        'unique_url': unique_url
    }

    return render(request, 'adminapp/script_creat.html', content)

@login_required(login_url='/auth/login/')
def script_edit(request, pk):
    title = 'внести изменения'

    script_to_edit = get_object_or_404(Script, pk=pk)
    control_tops = ControlTop.objects.filter(script=script_to_edit)
    controls_to_controls = ControlToControl.objects.filter(control__script=script_to_edit)
    situations = Situation.objects.filter(control__control__script=script_to_edit)

    # for control_top in control_tops:
    #     controls_to_controls[control_top]

    if request.method == 'POST':
        script_to_edit.name = request.POST['script_name']
        script_to_edit.save()
        return HttpResponseRedirect(reverse('admin:scripts_read'))


    # situations_list = Situation.objects.
    content = {
        'title': title,
        'script_to_edit': script_to_edit,
        'control_tops': control_tops,
        'controls_to_controls': controls_to_controls,
        'situations': situations
    }

    return render(request, 'adminapp/script_edit.html', content)

def script_activate(request, pk):
    pass

def script_deactivate(request, pk):
    pass

@login_required(login_url='/auth/login/')
def control_top_create(request, pk):
    title = 'добавить блок'

    script = get_object_or_404(Script, pk=pk)
    if request.method == 'POST':
        new_control_top = ControlTop(name=request.POST['control_name'], script=script)
        new_control_top.save()
        return HttpResponseRedirect(reverse('admin:script_edit', args=[script.pk]))

    content = {
        'title': title,
        'script': script
    }

    return render(request, 'adminapp/control_top_create.html', content)

@login_required(login_url='/auth/login/')
def control_top_edit(request, pk):
    title = 'добавить блок'

    control = get_object_or_404(ControlTop, pk=pk)
    if request.method == 'POST':
        control.name = request.POST['control_name']
        control.save()
        return HttpResponseRedirect(reverse('admin:script_edit', args=[control.script.pk]))

    content = {
        'title': title,
        'object': control

    }

    return render(request, 'adminapp/control_top_edit.html', content)

@login_required(login_url='/auth/login/')
def control_to_control_create(request, pk):
    title = 'создать подблок'

    control_top = get_object_or_404(ControlTop, pk=pk)
    if request.method == 'POST':
        new_control_to_control = ControlToControl(name=request.POST['control_name'], control=control_top)
        new_control_to_control.save()
        return HttpResponseRedirect(reverse('admin:script_edit', args=[control_top.script.pk]))

    content = {
        'title': title,
        'control_top': control_top
    }

    return render(request, 'adminapp/control_to_control_create.html', content)

@login_required(login_url='/auth/login/')
def control_to_control_edit(request, pk):
    title = 'изменить подблок'

    control = get_object_or_404(ControlToControl, pk=pk)
    if request.method == 'POST':
        control.name = request.POST['control_name']
        control.save()
        return HttpResponseRedirect(reverse('admin:script_edit', args=[control.control.script.pk]))

    content = {
        'title': title,
        'control': control
    }

    return render(request, 'adminapp/control_to_control_edit.html', content)

@login_required(login_url='/auth/login/')
def situation_create(request, pk):
    title = 'добавляем ситуацию'

    control_to_control = get_object_or_404(ControlToControl, pk=pk)
    if request.method == 'POST':
        new_situation = Situation(situation=request.POST['situation'],
                                  recomended_action=request.POST['recomended_action'],
                                  control=control_to_control)
        new_situation.save()
        return HttpResponseRedirect(reverse('admin:script_edit', args=[control_to_control.control.script.pk]))

    content = {
        'title': title,
        'control_to_control': control_to_control
    }

    return render(request, 'adminapp/situation_create.html', content)

@login_required(login_url='/auth/login/')
def situation_edit(request, pk):
    title = 'изменить ситуацию'

    situation = get_object_or_404(Situation, pk=pk)
    if request.method == 'POST':
        situation.situation = request.POST['situation']
        situation.recomended_action = request.POST['recomended_action']
        situation.save()
        return HttpResponseRedirect(reverse('admin:script_edit', args=[situation.control.control.script.pk]))

    content = {
        'title': title,
        'situation': situation
    }

    return render(request, 'adminapp/situation_edit.html', content)