from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import translation
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from ..forms.login import LoginForm

class LoginView(LoginView):
    form_class    = LoginForm
    template_name = 'main_app/login/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main_app:top'))
        else:
            return super().get(request)

class LoginRedirectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # ユーザーの言語コードを取得
        user_language = translation.get_language_from_request(request)
        print(user_language)
        # 言語コードに基づいてリダイレクト先を設定
        if user_language == 'ja':
            return redirect('/top/')
        elif user_language == 'en':
            return redirect('/en/top/')
        else:
            # デフォルトは設定ファイルの言語にリダイレクト
            return redirect(f'/top/')