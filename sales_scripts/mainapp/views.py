from datetime import timedelta, datetime, timezone

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.models import ScriptsUser
from adminapp.models import Script, ControlTop, ControlToControl, Situation
import adminapp.views as adminapp

# Create your views here.

def main(request):
    title = 'главная'

    content = {
        'title': title
    }

    return render(request, 'mainapp/index.html', content)

def script_view(request, script_url):
    title = 'Ваш скрипт'

    script = get_object_or_404(Script, url=script_url)
    controls_top = ControlTop.objects.filter(script=script)
    controls_to_controls = ControlToControl.objects.filter(control__script=script)
    situations = Situation.objects.filter(control__control__script=script)
    user = get_object_or_404(ScriptsUser, pk=script.user.pk)
    print(user.username)

    content = {
        'title': title,
        'controls_top':controls_top,
        'controls_to_controls': controls_to_controls,
        'situations': situations

    }

    adminapp.check_transaction(request, user)

    if request.user.is_authenticated or script.is_active:
        return render(request, 'mainapp/script_view.html', content)

    else:
        return render(request, 'mainapp/script_not_active.html', content)

def script_preview(request, pk):
    title = 'Ваш скрипт'

    script = get_object_or_404(Script, pk=pk)
    controls_top = ControlTop.objects.filter(script=script)
    controls_to_controls = ControlToControl.objects.filter(control__script=script)
    situations = Situation.objects.filter(control__control__script=script)

    delay = timedelta(hours=2)

    is_authorised = script.last_modified + delay > datetime.now(timezone.utc)

    content = {
        'title': title,
        'script': script,
        'controls_top': controls_top,
        'controls_to_controls': controls_to_controls,
        'situations': situations,
        'time_in': is_authorised

    }

    return render(request, 'mainapp/script_preview.html', content)
