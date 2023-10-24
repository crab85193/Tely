from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from ..forms.login import LoginForm

class LoginView(LoginView):
    form_class    = LoginForm
    template_name = 'main_app/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main_app:top'))
        else:
            return super().get(request)
