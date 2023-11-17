from django.http import HttpResponse
from django.views import View
from twilio.rest import Client
from ..call_manager import CallManager
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse

@method_decorator(csrf_exempt, name='dispatch')
class TwilioButtonView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(f"Twilio Button View")

    def post(self, request, *args, **kwargs):
        next_url = f"{'{0}://{1}'.format(self.request.scheme, self.request.get_host())}{reverse('main_app:twilio_gather_response')}"
        call_manager = CallManager()
        result = call_manager.gather("ボタンを押して下さい","09055169212",next_url)

        return HttpResponse(f"Call initiated with SID: {result}")


class HandleButtonView(View):
    def get(self, request, *args, **kwargs):
        digit_pressed = request.GET.get("Digits", None)

        # Twilioのレスポンスを初期化
        response = f'<Response>'

        # プッシュボタンの結果に応じて処理を行う
        if digit_pressed == "1":
            # ボタン1が押された場合の処理
            response += '<Say>You pressed button 1. Thank you!</Say>'
            # ここに続きのメッセージを追加する
            response += '<Say>This is the additional message after pressing button 1.</Say>'
        elif digit_pressed == "2":
            # ボタン2が押された場合の処理
            response += '<Say>You pressed button 2. Thank you!</Say>'
            # ここに続きのメッセージを追加する
            response += '<Say>This is the additional message after pressing button 2.</Say>'
        # 他のボタンに対する処理も同様に追加する

        # Twilioのレスポンスを閉じる
        response += '</Response>'

        return HttpResponse(response, content_type='text/xml')
