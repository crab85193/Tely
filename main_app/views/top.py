from django.views.generic import TemplateView

class TopView(TemplateView):
    template_name = 'main_app/index.html'
    