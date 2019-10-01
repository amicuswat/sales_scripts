import mainapp.views as mainapp
from django.urls import path
from django.conf.urls import include

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main, name='main_page'),
    path('view/<script_url>', mainapp.script_view, name='script_view'),
    path('preview/<int:pk>', mainapp.script_preview, name='script_preview'),
    path('i18n/', include('django.conf.urls.i18n')),
]
