import datetime
from django.utils import timezone
from zoneinfo import ZoneInfo
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from twilio.rest import Client
from ..call_manager import CallManager
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
from ..models.reservation import ReservationParent, ReservationChild

@method_decorator(csrf_exempt, name='dispatch')
class TwilioButtonView(View):
    def create_message(self, reservation_id):
        # 予約情報
        obj = ReservationParent.objects.get(id=reservation_id)
        r_datetime   = obj.reservation_datetime.astimezone(ZoneInfo(key='Asia/Tokyo'))
        r_year       = r_datetime.year
        r_month      = r_datetime.month
        r_day        = r_datetime.day
        r_hour       = r_datetime.hour
        r_minute     = r_datetime.minute
        r_num_people = obj.num_people
        r_name       = obj.representative_name
        r_memo       = obj.memo

        # 現在の日時
        n_datetime = datetime.datetime.now(ZoneInfo(key='Asia/Tokyo'))
        n_year = n_datetime.year
        n_month = n_datetime.month
        n_day = n_datetime.day

        message = f"こんにちは、電話予約の代理アプリ、テリーです。"

        if n_year == r_year and n_month == r_month and n_day == r_day:
            message += f"本日の"
        elif n_year == r_year and n_month == r_month:
            message += f"こんげつ{r_day}日の"
        elif n_year == r_year:
            message += f"{r_month}月{r_day}日の"
        else:
            message += f"{r_year}年{r_month}月{r_day}日の"

        if r_minute == 0:
            message += f"{r_hour}時に"
        elif r_minute == 30:
            message += f"{r_hour}時半に"
        else:
            message += f"{r_hour}時{r_minute}分に"
        
        message += f"{r_num_people}名、代表者名は、{r_name}で予約を取りたいのですが、可能でしょうか。" 
        
        if r_memo:
            message += f"以下はお客様から、店舗様への伝達メッセージです。{r_memo}。"

        message += f"予約可能の場合は1を、予約が不可能の場合は2を、この音声をもう1度聞く場合は3を押して下さい。"

        return message

    def get(self, request, reservation_id, *args, **kwargs):
        next_url = f"{'{0}://{1}'.format(self.request.scheme, self.request.get_host())}{reverse('main_app:twilio_gather_response')}"
        call_manager = CallManager()

        message = self.create_message(reservation_id)

        obj_parent = ReservationParent.objects.get(id=reservation_id)

        # sid = call_manager.gather(message, obj_parent.shop_tel_number, next_url)
        sid = call_manager.gather(message, "09055169212", next_url)

        obj_parent.sid = sid
        obj_parent.save()

        obj_child = ReservationChild.objects.create(
            parent  = obj_parent,
            status  = ReservationChild.SUCCESS,
            title   = '電話発信を行いました',
            message = '店舗様へ電話の発信を行いました。店舗様からの返答をお待ちください。'
        )

        return HttpResponseRedirect(reverse('main_app:reservation_done'))


class HandleButtonView(View):
    def get(self, request, *args, **kwargs):
        next_url = f"{'{0}://{1}'.format(self.request.scheme, self.request.get_host())}{reverse('main_app:twilio_gather_response')}"
        call_manager = CallManager()
        
        digit_pressed = request.GET.get("Digits", None)
        sid = request.GET.get("CallSid", None)
        obj_parent = ReservationParent.objects.get(sid=sid)
        
        if digit_pressed == "1":
            message = "予約受付ありがとうございました。本日の21時から3名で、よろしくお願いします。"
            response = call_manager.create_say_response_xml(message)

            obj_child = ReservationChild.objects.create(
                parent  = obj_parent,
                status  = ReservationChild.SUCCESS,
                title   = '予約受付が承認しました',
                message = '店舗様が予約受付が承認しました。'
            )

            obj_child = ReservationChild.objects.create(
                parent  = obj_parent,
                status  = ReservationChild.END,
                title   = '代理予約が完了しました',
                message = '代理予約処理が完了しました。'
            )

            obj_parent.is_end = True
            obj_parent.end_datetime = timezone.now()
            obj_parent.save()

        elif digit_pressed == "2":
            message = "承知いたしました。また機会があればよろしくお願いします。"
            response = call_manager.create_say_response_xml(message)

            obj_child = ReservationChild.objects.create(
                parent  = obj_parent,
                status  = ReservationChild.FAILURE,
                title   = '予約受付が承認されませんでした',
                message = '店舗様が予約受付が承認しませんでした。'
            )

            obj_child = ReservationChild.objects.create(
                parent  = obj_parent,
                status  = ReservationChild.END,
                title   = '代理予約が完了しました',
                message = '代理予約処理が完了しました。'
            )

            obj_parent.is_end = True
            obj_parent.end_datetime = timezone.now()
            obj_parent.save()

        else:
            message = "こんにちは。本日の21時から3名で予約を取りたいのですが、可能でしょうか。予約可能の場合は1を、予約が不可能の場合は2を、この音声をもう1度聞く場合は3を押して下さい。"
            response = call_manager.create_gather_response_xml(message, next_url)

            obj_child = ReservationChild.objects.create(
                parent  = obj_parent,
                status  = ReservationChild.WAIT,
                title   = '通話中',
                message = 'ただいま通話中です。しばらくお待ちください。'
            )
        

        return HttpResponse(response, content_type='text/xml')
