from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-user'
        
        self.fields['username'].widget.attrs['placeholder'] = 'email'
        self.fields['password'].widget.attrs['placeholder'] = 'password'
