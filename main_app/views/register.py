from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView
from ..models.user import User
from ..models.user_activate_tokens import UserActivateTokens
from ..forms.register import Register
from django.contrib import messages

class RegisterRequestView(CreateView):
    form_class    = Register
    template_name = 'main_app/register/register-request.html'
    success_url   = reverse_lazy("main_app:register_done")

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main_app:top'))
        else:
            return super().get(request)

    def form_valid(self, form):
        instance = form.save()
        
        user_activate_token = UserActivateTokens.objects.create(
            user=instance,
            expired_at=datetime.now() + timedelta(days=settings.ACTIVATION_EXPIRED_DAYS),
        )

        subject = '【Tely】アカウントの認証'
        message = f"こんにちは {instance.username} さん\n\nご登録いただきありがとうございます。アカウントを有効化するためには、以下のリンクをクリックしてください。\n\n{'{0}://{1}'.format(self.request.scheme, self.request.get_host())}{reverse('main_app:register_complete', args=[user_activate_token.activate_token])}\n\nもしこのメールが誤って届いた場合や、アカウント登録を行っていない場合は、このメールを無視していただいて結構です。\n\nご質問やお困りごとがあれば、お気軽にご連絡ください。\n\n[Tely] サポートチーム\n"

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [
            instance.email,
        ]

        send_mail(subject, message, from_email, recipient_list)

        return HttpResponseRedirect(reverse('main_app:register_done', args=[user_activate_token.user.id]))


class RegisterDoneView(TemplateView):
    template_name = 'main_app/register/register-done.html'
    user_id = None

    def get(self, request, user_id):
        self.user_id = user_id
        return super().get(request)
    
    def post(self, request, user_id):
        instance = User.objects.get(id=str(user_id))
        user_activate_token = UserActivateTokens.objects.get(user=instance)
        subject = '【Tely】アカウントの認証'
        message = f"こんにちは {instance.username} さん\n\nご登録いただきありがとうございます。アカウントを有効化するためには、以下のリンクをクリックしてください。\n\n{'{0}://{1}'.format(self.request.scheme, self.request.get_host())}{reverse('main_app:register_complete', args=[user_activate_token.activate_token])}\n\nもしこのメールが誤って届いた場合や、アカウント登録を行っていない場合は、このメールを無視していただいて結構です。\n\nご質問やお困りごとがあれば、お気軽にご連絡ください。\n\n[Tely] サポートチーム\n"

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [
            instance.email,
        ]

        send_mail(subject, message, from_email, recipient_list)
        
        messages.success(request, 'メールを再送しました。ご確認ください。')

        return super().get(request)
    

class RegisterCompleteView(TemplateView):
    template_name = 'main_app/register/register-complete.html'

    def get(self, request, activate_token):
        activated_user = UserActivateTokens.objects.get_or_none(activate_token=activate_token)
        
        if activated_user:
            activated_user = UserActivateTokens.objects.activate_user_by_token(activate_token)
            
            if hasattr(activated_user, 'is_active'):
                if activated_user.is_active:
                    subject = '【Tely】アカウント登録が完了しました'
                    message = f"こんにちは {activated_user.username} さん\n\nアカウントの有効化が正常に完了しました。これにより、Tely のメンバーとしてアクセスが可能となります。\n\n{'{0}://{1}'.format(self.request.scheme, self.request.get_host())}{reverse('main_app:login')}\n\nもしご質問や不明点がありましたら、お気軽にご連絡ください。\nサイトをご利用いただく際には、安全なパスワードの使用やセキュリティにご注意いただくようお願いいたします。\n\nご登録いただき、ありがとうございます。\n\n[Tely] サポートチーム\n"

                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [
                        activated_user.email,
                    ]

                    send_mail(subject, message, from_email, recipient_list)

                    UserActivateTokens.objects.filter(activate_token=activate_token).delete()

                if not activated_user.is_active:
                    HttpResponseRedirect(reverse('main_app:register_error', args=[2]))
                    
            if not hasattr(activated_user, 'is_active'):
                message = 'エラーが発生しました'
                HttpResponseRedirect(reverse('main_app:register_error', args=[1]))

            return super().get(request)
        else:
            raise Http404
        
class RegisterErrorView(TemplateView):
    template_name = 'main_app/register/register-error.html'
    e_code = 0

    def get(self, request, error_code):
        self.e_code = error_code
        return super().get(request)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        match self.e_code:
            case 0:
                message = 'A serious error has occurred. Please contact the developer.'
            case 1:
                message = 'A serious error has occurred. Please contact the developer.'
            case 2:
                message = 'Activation failed. Please contact your developer.'
            case _:
                message = 'A serious error has occurred. Please contact the developer.'

        context['message'] = message

        return context