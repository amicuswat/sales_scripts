from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.models import ScriptsUser
from adminapp.models import Script, ControlTop, ControlToControl, Situation

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

    content = {
        'title': title,
        'controls_top':controls_top,
        'controls_to_controls': controls_to_controls,
        'situations': situations

    }

    if True:
        return render(request, 'mainapp/script_view.html', content)

    else:
        return render(request, 'mainapp/script_not_active.html', content)

