from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class TopView(LoginRequiredMixin, TemplateView):
    template_name = 'main_app/index.html'
    