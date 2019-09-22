from django.urls import path
import marketapp.views as marketapp

app_name = 'marketapp'

urlpatterns = [
    path('sd_shop/', marketapp.sd_shop, name='sd_shop'),
    path('buy/<int:amount>/<int:quantity>', marketapp.buy_sd, name='buy_sd'),
]