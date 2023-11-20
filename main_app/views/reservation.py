from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from ..call_manager import CallManager
from django.shortcuts import render


class ReservationPhoneView(LoginRequiredMixin, TemplateView):
    template_name = "main_app/reservation/reservation_phone.html"

    def post(self, request):
        call_manager = CallManager()
        call_manager.call("こんにちは。私は予約がしたい", request.POST['tel'])
        print(f"電話番号 : {request.POST['tel']}")
        
        return HttpResponseRedirect(reverse('main_app:reservation_done')) 
    

class ReservationDoneView(LoginRequiredMixin, TemplateView):
    template_name = "main_app/reservation/reservation-done.html"
    
class ReservationAddView(LoginRequiredMixin, TemplateView): #$①ログインしていないと見れない設定と　$②Templateからを使用してページをレンダリングする
    template_name = 'main_app/reservation/reservation_add.html'