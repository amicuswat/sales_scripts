from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.models import ScriptsUser, UserRights
from adminapp.models import Script, ControlTop, ControlToControl, Situation, Situation2D, SituationLinear
from marketapp.models import Transaction
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import random, string
from datetime import timedelta, datetime, timezone
import datetime as dt


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

    check_transaction(request, request.user)

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
    title = 'Мастерская скриптов'
    container_size = 'medium_container'
    rights = get_object_or_404(UserRights, user__pk=request.user.pk)
    message = '- Кэп, тут у нас кое что есть, можем с имеющимися скриптами поработать. Или новый замастрячить.'

    scripts_list = Script.objects.filter(user__username=request.user.username).order_by('-is_active', '-last_modified')

    content = {
        'title': title,
        'rights': rights,
        'scripts_list': scripts_list,
        'container_size': container_size,
        'message': message
    }

    return render(request, 'adminapp/scripts_read.html', content)


@login_required(login_url='/auth/login/')
def script_create(request, script_type):
    title = 'новый скрипт'
    container_size = 'small_container'
    rights = get_object_or_404(UserRights, user__pk=request.user.pk)

    if request.method == 'POST':
        new_script = Script(
            user=request.user, description=request.POST['description'],
            name=request.POST['script_name'], url=request.POST['url'],
            type=script_type
        )
        new_script.save()
        return HttpResponseRedirect(reverse('admin:scripts_read'))

    unique_url = randomword(16)

    content = {
        'title': title,
        'rights': rights,
        'container_size': container_size,
        'unique_url': unique_url,
        'type': script_type
    }

    return render(request, 'adminapp/script_creat.html', content)


@login_required(login_url='/auth/login/')
def script_edit(request, pk):
    title = 'внести изменения'
    container_size = 'large_container'

    script_to_edit = get_object_or_404(Script, pk=pk)
    script_type = script_to_edit.type

    rights = get_object_or_404(UserRights, user__pk=request.user.pk)

    if script_type == 3:
        control_tops = ControlTop.objects.filter(script=script_to_edit)
        controls_to_controls = ControlToControl.objects.filter(control__script=script_to_edit)
        situations = Situation.objects.filter(control__control__script=script_to_edit)

        content = {
            'title': title,
            'script_to_edit': script_to_edit,
            'control_tops': control_tops,
            'controls_to_controls': controls_to_controls,
            'situations': situations,
            'rights': rights,
            'container_size': container_size,
            'type': script_type
        }

    elif script_type == 2:
        control_tops = ControlTop.objects.filter(script=script_to_edit)
        situations = Situation2D.objects.filter(control_top__script=script_to_edit)

        content = {
            'title': title,
            'script_to_edit': script_to_edit,
            'control_tops': control_tops,
            'situations': situations,
            'rights': rights,
            'container_size': container_size,
            'type': script_type
        }
    else:
        situations = SituationLinear.objects.filter(script=script_to_edit)
        content = {
            'title': title,
            'script_to_edit': script_to_edit,
            'situations': situations,
            'rights': rights,
            'container_size': container_size,
            'type': script_type
        }

    if request.method == 'POST':
        script_to_edit.name = request.POST['script_name']
        script_to_edit.save()
        return HttpResponseRedirect(reverse('admin:scripts_read'))

    return render(request, 'adminapp/script_edit.html', content)


def check_transaction(request, user):
    print("Checking transaction")

    latest_transactions = Transaction.objects.filter(user=user).order_by('-date_created')

    if not latest_transactions:
        new_transaction = Transaction(user=user)
        return new_transaction
    else:
        latest_transaction = latest_transactions[0]

    days_passed = (datetime.now(timezone.utc) - latest_transaction.date_created).days


    # if today there is a transaction
    if days_passed == 0:
        return latest_transaction

    # if yesturday transaction
    elif days_passed == 1:
        if user.scripts_days >= user.scripts_used:
            user.scripts_days -= user.scripts_used
            user.save()
            new_transaction = Transaction(user=user, sd_burned=user.scripts_used)
            new_transaction.save()
            return new_transaction
        else:
            new_transaction = Transaction(user=user, sd_burned=0)
            new_transaction.save()
            user.scripts_used = 0
            user.save()
            scripts_list = Script.objects.filter(user__pk=user.pk, is_active=True)
            for each_script in scripts_list:
                each_script.is_active = False
                each_script.save()
            return new_transaction

    # more days passed
    else:
        # create a transaction for every day till today
        for i in range(days_passed):
            new_transaction_date = latest_transaction.date_created + timedelta(days=1)
            if i + 1 == days_passed:
                new_transaction_date = datetime.now(timezone.utc)

            if user.scripts_days >= user.scripts_used:

                new_transaction =  Transaction(user=user, sd_burned=user.scripts_used, date_created=new_transaction_date)
                new_transaction.save()
                latest_transaction = new_transaction
                user.scripts_days -= user.scripts_used
                user.save()
            else:
                new_transaction = Transaction(user=user, sd_burned=0, date_created=new_transaction_date)
                new_transaction.save()
                latest_transaction = new_transaction
                user.scripts_used = 0
                user.save()
                scripts_list = Script.objects.filter(user__pk=user.pk, is_active=True)
                for each_script in scripts_list:
                    each_script.is_active = False
                    each_script.save()


        # if sd id not enough deactivate scripts and create 0 sd transactions
        return latest_transaction



def script_activate(request, pk):
    user = request.user

    script = get_object_or_404(Script, pk=pk)
    success = '- Норма Кэп, скрипт активирован. Какие еще будут приказы?'
    failure = '- Ничего не выйдет, Кэп. Бак пуст, без сд не взлетим.'
    message = ''

    title = 'Мастерская скриптов'
    container_size = 'medium_container'
    rights = get_object_or_404(UserRights, user__pk=request.user.pk)

    scripts_list = Script.objects.filter(user__username=request.user.username).order_by('-is_active', '-last_modified')

    latest_transaction = check_transaction(request, user)

    if user.scripts_used < latest_transaction.sd_burned:
        script.is_active = True
        script.save()
        user.scripts_used += 1
        user.save()

        message = success
    elif user.scripts_days > 0:
        latest_transaction.sd_burned += 1
        latest_transaction.save()
        # activating script
        script.is_active = True
        script.save()
        # change user data
        user.scripts_days -= 1
        user.scripts_used += 1
        user.save()
        message = success
    else:
        message = failure

    content = {
        'title': title,
        'rights': rights,
        'scripts_list': scripts_list,
        'container_size': container_size,
        'message': message
    }

    return render(request, 'adminapp/scripts_read.html', content)


def script_deactivate(request, pk):
    user = request.user

    script = get_object_or_404(Script, pk=pk)

    message = '- Кэп, приказ выполнен, скрипт деактивирован!'

    title = 'Мастерская скриптов'
    container_size = 'medium_container'
    rights = get_object_or_404(UserRights, user__pk=request.user.pk)

    script.is_active = False
    script.save()
    user.scripts_used -= 1
    user.save()

    scripts_list = Script.objects.filter(user__username=request.user.username).order_by('-is_active', '-last_modified')

    content = {
        'title': title,
        'rights': rights,
        'scripts_list': scripts_list,
        'container_size': container_size,
        'message': message
    }

    return render(request, 'adminapp/scripts_read.html', content)


@login_required(login_url='/auth/login/')
def control_top_create(request, pk):
    title = 'добавить блок'
    container_size = 'small_container'
    rights = get_object_or_404(UserRights, user__pk=request.user.pk)

    script = get_object_or_404(Script, pk=pk)
    same_controls_count = ControlTop.objects.filter(script=script).count()

    if request.method == 'POST':
        new_control_top = ControlTop(name=request.POST['control_name'], script=script, position=same_controls_count)
        new_control_top.save()
        script.save()
        return HttpResponseRedirect(reverse('admin:script_edit', args=[script.pk]))

    content = {
        'title': title,
        'script': script,
        'rights': rights,
        'container_size': container_size
    }

    return render(request, 'adminapp/control_top_create.html', content)


@login_required(login_url='/auth/login/')
def control_top_edit(request, pk):
    title = 'добавить блок'
    container_size = 'small_container'
    rights = get_object_or_404(UserRights, user__pk=request.user.pk)

    control = get_object_or_404(ControlTop, pk=pk)
    if request.method == 'POST':
        control.name = request.POST['control_name']
        control.save()
        return HttpResponseRedirect(reverse('admin:script_edit', args=[control.script.pk]))

    content = {
        'title': title,
        'object': control,
        'rights': rights,
        'container_size': container_size

    }

    return render(request, 'adminapp/control_top_edit.html', content)


@login_required(login_url='/auth/login/')
def control_to_control_create(request, pk):
    title = 'создать подблок'
    container_size = 'small_container'
    rights = get_object_or_404(UserRights, user__pk=request.user.pk)

    control_top = get_object_or_404(ControlTop, pk=pk)
    script = get_object_or_404(Script, pk=control_top.script.pk)
    same_controls_count = ControlToControl.objects.filter(control=control_top).count()

    if request.method == 'POST':
        new_control_to_control = ControlToControl(name=request.POST['control_name'], control=control_top,
                                                  position=same_controls_count)
        new_control_to_control.save()
        script.save()
        return HttpResponseRedirect(reverse('admin:script_edit', args=[control_top.script.pk]))

    content = {
        'title': title,
        'control_top': control_top,
        'rights': rights,
        'container_size': container_size
    }

    return render(request, 'adminapp/control_to_control_create.html', content)


@login_required(login_url='/auth/login/')
def control_to_control_edit(request, pk):
    title = 'изменить подблок'
    container_size = 'small_container'
    rights = get_object_or_404(UserRights, user__pk=request.user.pk)

    control = get_object_or_404(ControlToControl, pk=pk)
    if request.method == 'POST':
        control.name = request.POST['control_name']
        control.save()
        return HttpResponseRedirect(reverse('admin:script_edit', args=[control.control.script.pk]))

    content = {
        'title': title,
        'control': control,
        'rights': rights,
        'container_size': container_size
    }

    return render(request, 'adminapp/control_to_control_edit.html', content)


@login_required(login_url='/auth/login/')
def situation_create(request, pk, script_type):
    title = 'добавляем ситуацию'
    container_size = 'small_container'
    rights = get_object_or_404(UserRights, user__pk=request.user.pk)

    content = {
        'title': title,
        'rights': rights,
        'container_size': container_size,
        'type': script_type
    }

    if script_type == 3:
        control_to_control = get_object_or_404(ControlToControl, pk=pk)
        script = get_object_or_404(Script, pk=control_to_control.control.script.pk)
        same_situations_count = Situation.objects.filter(control=control_to_control).count()
        content['control_to_control'] = control_to_control

        if request.method == 'POST':
            new_situation = Situation(situation=request.POST['situation'],
                                      recomended_action=request.POST['recomended_action'],
                                      control=control_to_control,
                                      position=same_situations_count)
            new_situation.save()
            script.save()
            return HttpResponseRedirect(reverse('admin:script_edit', args=[control_to_control.control.script.pk]))

        return render(request, 'adminapp/situation_create.html', content)

    elif script_type == 2:
        control_top = get_object_or_404(ControlTop, pk=pk)
        script = get_object_or_404(Script, pk=control_top.script.pk)
        same_situations_count = Situation2D.objects.filter(control_top=control_top).count()
        content['control_top'] = control_top

        if request.method == 'POST':
            new_situation = Situation2D(situation=request.POST['situation'],
                                        recomended_action=request.POST['recomended_action'],
                                        control_top=control_top,
                                        position=same_situations_count)
            new_situation.save()
            script.save()
            return HttpResponseRedirect(reverse('admin:script_edit', args=[control_top.script.pk]))

        return render(request, 'adminapp/situation2d_create.html', content)


    else:
        script = get_object_or_404(Script, pk=pk)
        same_situations_count = SituationLinear.objects.filter(script=script).count()
        content['script'] = script

        if request.method == 'POST':
            new_situation = SituationLinear(situation=request.POST['situation'],
                                            recomended_action=request.POST['recomended_action'],
                                            script=script,
                                            position=same_situations_count)
            new_situation.save()
            script.save()
            return HttpResponseRedirect(reverse('admin:script_edit', args=[script.pk]))

        return render(request, 'adminapp/situation_linear_create.html', content)


@login_required(login_url='/auth/login/')
def situation_edit(request, pk, script_type):
    title = 'изменить ситуацию'
    container_size = 'small_container'
    rights = get_object_or_404(UserRights, user__pk=request.user.pk)

    if script_type == 3:
        situation = get_object_or_404(Situation, pk=pk)
        script_pk = situation.control.control.script.pk
    elif script_type == 2:
        situation = get_object_or_404(Situation2D, pk=pk)
        script_pk = situation.control_top.script.pk
    else:
        situation = get_object_or_404(SituationLinear, pk=pk)
        script_pk = situation.script.pk


    if request.method == 'POST':
        situation.situation = request.POST['situation']
        situation.recomended_action = request.POST['recomended_action']
        situation.save()
        return HttpResponseRedirect(reverse('admin:script_edit', args=[script_pk]))

    content = {
        'title': title,
        'situation': situation,
        'rights': rights,
        'container_size': container_size
    }

    return render(request, 'adminapp/situation_edit.html', content)
