import mainapp.views as mainapp
from django.urls import path

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main, name='main_page'),
    path('view/<script_url>', mainapp.script_view, name='script_view'),
]