from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models.user import User
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'main_app/user-settings.html'

    def post(self, request):
        instance = User.objects.get(id=request.user.id)

        instance.username = request.POST["username"]
        instance.email = request.POST["email"]

        instance.save()

        messages.success(request, _("Changes have been completed."))

        return redirect("main_app:user_settings")
    