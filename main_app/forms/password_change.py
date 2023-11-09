from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class PasswordChange(PasswordChangeForm):
    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-user'

        self.fields['old_password'].widget.attrs['placeholder']  = 'Old Password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Retype New Password'
