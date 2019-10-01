from datetime import timedelta, datetime, timezone

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.models import ScriptsUser
from adminapp.models import Script, ControlTop, ControlToControl, Situation, Situation2D, SituationLinear
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
    user = get_object_or_404(ScriptsUser, pk=script.user.pk)

    title += " - " + script.name

    adminapp.check_transaction(request, user)

    content = {
        'title': title,
        'script': script
    }

    if not script.is_active:
        return render(request, 'mainapp/script_not_active.html', content)

    if script.type == 3:

        controls_top = ControlTop.objects.filter(script=script)
        controls_to_controls = ControlToControl.objects.filter(control__script=script)
        situations = Situation.objects.filter(control__control__script=script)

        content['controls_top'] = controls_top
        content['controls_to_controls'] = controls_to_controls
        content['situations'] = situations

        return render(request, 'mainapp/script_view.html', content)

    elif script.type == 2:

        controls_top = ControlTop.objects.filter(script=script)
        situations = Situation2D.objects.filter(control_top__script=script)

        content['controls_top'] = controls_top
        content['situations'] = situations

        return render(request, 'mainapp/script2d_view.html', content)

    else:

        situations = SituationLinear.objects.filter(script=script)

        content['situations'] = situations

        return render(request, 'mainapp/script_linear_view.html', content)


def script_preview(request, pk):
    title = 'Ваш скрипт'

    script = get_object_or_404(Script, pk=pk)

    title += " - " + script.name

    delay = timedelta(minutes=30)

    is_authorised = script.last_modified + delay > datetime.now(timezone.utc)

    if script.type == 3:
        controls_top = ControlTop.objects.filter(script=script)
        controls_to_controls = ControlToControl.objects.filter(control__script=script)
        situations = Situation.objects.filter(control__control__script=script)

        content = {
            'title': title,
            'script': script,
            'controls_top': controls_top,
            'controls_to_controls': controls_to_controls,
            'situations': situations,
            'time_in': is_authorised

        }

        return render(request, 'mainapp/script_preview.html', content)

    elif script.type == 2:
        controls_top = ControlTop.objects.filter(script=script)
        situations = Situation2D.objects.filter(control_top__script=script)

        content = {
            'title': title,
            'script': script,
            'controls_top': controls_top,
            'situations': situations,
            'time_in': is_authorised

        }

        return render(request, 'mainapp/script2d_preview.html', content)

    else:

        situations = SituationLinear.objects.filter(script=script)

        content = {
            'title': title,
            'script': script,
            'situations': situations,
            'time_in': is_authorised

        }

        return render(request, 'mainapp/script_linear_preview.html', content)





