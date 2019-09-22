import adminapp.views as adminapp
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('control_post/', adminapp.control_post, name='control_post'),

    path('scripts/read', adminapp.scripts_read, name='scripts_read'),
    path('script/create', adminapp.script_create, name='script_create'),
    path('script/edit/<int:pk>', adminapp.script_edit, name='script_edit'),

    path('control_top/create/<int:pk>', adminapp.control_top_create, name='control_top_create'),
    path('control_top/edit/<int:pk>', adminapp.control_top_edit, name='control_top_edit'),

    path('control_to_control/create/<int:pk>', adminapp.control_to_control_create, name='control_to_control_create'),
    path('control_to_control/edit/<int:pk>', adminapp.control_to_control_edit, name='control_to_control_edit'),

    path('situation/create/<int:pk>', adminapp.situation_create, name='situation_create'),
    path('situation/edit/<int:pk>', adminapp.situation_edit, name='situation_edit'),

]