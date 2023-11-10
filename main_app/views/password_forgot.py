from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from ..forms.password_forgot import PasswordForgotForm, SetNewPasswordForm

class PasswordForgotView(PasswordResetView):
    template_name = 'main_app/password_forgot/password_forgot.html'
    subject_template_name = 'main_app/mail_templates/password_reset/subject.txt'
    email_template_name   = 'main_app/mail_templates/password_reset/message.txt'
    form_class = PasswordForgotForm
    success_url = reverse_lazy('main_app:password_forgot_done')


class PasswordForgotDoneView(PasswordResetDoneView):
    template_name = 'main_app/password_forgot/password_forgot_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main_app/password_forgot/password_reset_confirm.html'
    form_class = SetNewPasswordForm
    success_url = reverse_lazy('main_app:password_reset_complete')

class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'main_app/password_forgot/password_reset_complete.html'
