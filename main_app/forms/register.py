from django.contrib.auth.forms import UserCreationForm
from ..models.user import User

class Register(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-user'
        
        self.fields['email'].widget.attrs['placeholder']     = 'Mail Address'
        self.fields['username'].widget.attrs['placeholder']  = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Retype Password'