from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from twilio.rest import Client
from ..call_manager import CallManager
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse

@method_decorator(csrf_exempt, name='dispatch')
class TwilioButtonView(View):
    def get(self, request, *args, **kwargs):
        next_url = f"{'{0}://{1}'.format(self.request.scheme, self.request.get_host())}{reverse('main_app:twilio_gather_response')}"
        call_manager = CallManager()

        message = "こんにちは。本日の21時から3名、代表者名は「神村」で予約を取りたいのですが、可能でしょうか。予約可能の場合は1を、予約が不可能の場合は2を、この音声をもう1度聞く場合は3を押して下さい。"

        result = call_manager.gather(message, "09055169212", next_url)

        return HttpResponseRedirect(reverse('main_app:reservation_done'))


class HandleButtonView(View):
    def get(self, request, *args, **kwargs):
        next_url = f"{'{0}://{1}'.format(self.request.scheme, self.request.get_host())}{reverse('main_app:twilio_gather_response')}"
        call_manager = CallManager()
        
        digit_pressed = request.GET.get("Digits", None)
        
        if digit_pressed == "1":
            message = "予約受付ありがとうございました。本日の21時から3名で、よろしくお願いします。"
            response = call_manager.create_say_response_xml(message)
        elif digit_pressed == "2":
            message = "承知いたしました。また機会があればよろしくお願いします。"
            response = call_manager.create_say_response_xml(message)
        else:
            message = "こんにちは。本日の21時から3名で予約を取りたいのですが、可能でしょうか。予約可能の場合は1を、予約が不可能の場合は2を、この音声をもう1度聞く場合は3を押して下さい。"
            response = call_manager.create_gather_response_xml(message, next_url)
        

        return HttpResponse(response, content_type='text/xml')
