from django.contrib.auth.forms import AuthenticationForm
from .models import ScriptsUser


class ScriptsUserLoginForm(AuthenticationForm):
    class Meta:
        model = ScriptsUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ScriptsUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class']='form-control'
            field.help_text = ''