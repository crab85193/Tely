from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class InputReserveView(LoginRequiredMixin, TemplateView): #$①ログインしていないと見れない設定と　$②Templateからを使用してページをレンダリングする
    template_name = 'main_app/reservation/input_reserve.html'
    
    