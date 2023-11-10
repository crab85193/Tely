from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class PasswordForgotForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-user'
        
        self.fields['email'].widget.attrs['placeholder']  = 'Enter Email Address...'
 

class SetNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-user'

        self.fields['new_password1'].widget.attrs['placeholder']  = 'Enter New password...'
        self.fields['new_password2'].widget.attrs['placeholder']  = 'Enter New password confirmation...'