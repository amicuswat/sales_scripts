from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from authapp.models import ScriptsUser
from marketapp.models import Purchase, Transaction, InvoiceRequest
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/auth/login/')
def buy_sd(request, price, quantity):

    # user = get_object_or_404(ScriptsUser, pk=request.user.pk)
    # user.scripts_days += quantity
    # user.save()
    # purchase = Purchase(user=user, sd_bought=quantity, rubles_payed=amount)
    # purchase.save()

    return HttpResponseRedirect(reverse('admin:control_post'))


@login_required(login_url='/auth/login/')
def request_invoice(request, price, quantity):
    title = 'Запрос на выставление счета'
    user = request.user
    to_pay = price * quantity

    content = {
        'title': title,
        'price': price,
        'quantity': quantity,
        'to_pay': to_pay,
        'user': user

    }

    if request.method == 'POST':
        new_order = InvoiceRequest(user=user, price_per_sd=price,
                                   quantity_sd=quantity, comment=request.POST['comment'],
                                   to_pay=to_pay)
        new_order.save()
        return HttpResponseRedirect(reverse('admin:control_post'))

    return render(request, 'marketapp/request_invoice.html', content)

@login_required(login_url='/auth/login/')
def sd_shop(request):
    title = 'Магазин с/д'
    container_size = 'medium_container'
    prices = [
        {
            'volume': 20,
            'price': 12,
            'economy': 0,
            'to_pay': 240,
            'message': 'Кэп, ну как то так, далеко не улетим, да и дорого, чисто попробовать.'
        },
        {
            'volume': 50,
            'price': 11,
            'economy': 50,
            'to_pay': 550,
            'message': 'Кэп, ну это уже куда не шло, месячишку полетаем, да и на чупачупс сэкономим.'
        },
        {
            'volume': 100,
            'price': 10,
            'economy': 200,
            'to_pay': 1000,
            'message': 'Кэп, можно брать, на несколько полетов хватит, и еще детям на конфетки останется.'
        },
        {
            'volume': 250,
            'price': 9,
            'economy': 750,
            'to_pay': 2250,
            'message': 'Кэп, отличный выбор, и не дорого и нормально полетать можно.'
        },
        {
            'volume': 500,
            'price': 8,
            'economy': 2000,
            'to_pay': 4000,
            'message': 'Кэп, то что надо. Грузить? Нам на долго хватит и еще на пол столько же останется.'
        },
        {
            'volume': 1000,
            'price': 7,
            'economy': 5000,
            'to_pay': 7000,
            'message': 'Кэп, да мы с такими запасами... Эээххх... И не дорого совсе.'
        },
        {
            'volume': 5000,
            'price': 6,
            'economy': 30000,
            'to_pay': 30000,
            'message': 'Кэп, нам этого на всю жизнь хватит и внукам останется, надо брать. Да и бесплатно почти отдают.'
        },
    ]

    content = {
        'title': title,
        'container_size': container_size,
        'prices': prices
    }

    return render(request, 'marketapp/sd_shop.html', content)
