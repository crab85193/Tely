from django.views.generic import TemplateView

class ProductInfoView(TemplateView):
    template_name = 'main_app/product_info.html'
    