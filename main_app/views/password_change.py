from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ..forms.password_change import PasswordChange

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChange
    success_url = reverse_lazy('main_app:password_change_done')
    template_name = 'main_app/password_change/password_change.html' 
    
class PasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'main_app/password_change/password_change_done.html'
    