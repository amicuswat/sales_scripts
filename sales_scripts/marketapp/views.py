from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from authapp.models import ScriptsUser

# Create your views here.

def buy_sd(request, amount, quantity):
    title = 'Магазин с/д'

    user = get_object_or_404(ScriptsUser, pk=request.user.pk)
    user.scripts_days += quantity
    user.save()

    content ={
        'title': title
    }
    return HttpResponseRedirect(reverse('admin:control_post'))

def sd_shop(request):
    title = 'Магазин с/д'

    content = {
        'title': title
    }

    return render(request, 'marketapp/sd_shop.html', content)
