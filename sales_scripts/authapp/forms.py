from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import ScriptsUser
from django import forms



class ScriptsUserLoginForm(AuthenticationForm):
    class Meta:
        model = ScriptsUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ScriptsUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ScriptsUserRegisterForm(UserCreationForm):
    class Meta:
        model = ScriptsUser
        fields = ('username', 'first_name', 'password1', 'password2',
                  'email', )

    def __init__(self, *args, **kwargs):
        super(ScriptsUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

class ScriptsUserEditForm(UserChangeForm):
    class Meta:
        model = ScriptsUser
        fields = ('username', 'first_name', 'password',
                  'email', )

    def __init__(self, *args, **kwargs):
        super(ScriptsUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()