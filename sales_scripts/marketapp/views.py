from django.shortcuts import render

# Create your views here.

def buy_sd(request, money, quantity):
    title = 'Магазин с/д'

    content ={
        'title': title
    }
    pass

def sd_shop(request):
    title = 'Магазин с/д'

    content = {
        'title': title
    }

    return render(request, 'marketapp/sd_shop.html', content)
