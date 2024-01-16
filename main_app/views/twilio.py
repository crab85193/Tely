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
from ..models.notice import UserNotice

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

        sid = call_manager.gather(message, obj_parent.shop_tel_number, next_url)

        obj_parent.sid = sid
        obj_parent.save()

        obj_child = ReservationChild.objects.create(
            parent     = obj_parent,
            status     = ReservationChild.SUCCESS,
            title_ja   = '電話発信を行いました',
            title_en   = 'Phone outgoing calls were made',
            message_ja = '店舗様へ電話の発信を行いました。店舗様からの返答をお待ちください。',
            message_en = 'We have made a phone call to the store. Please wait for a response from the store.',
        )

        return HttpResponseRedirect(reverse('main_app:reservation_done'))


@method_decorator(csrf_exempt, name='dispatch')
class HandleButtonView(View):
    def post(self, request, *args, **kwargs):
        next_url = f"{'{0}://{1}'.format(self.request.scheme, self.request.get_host())}{reverse('main_app:twilio_gather_response')}"
        call_manager = CallManager()
        
        digit_pressed = request.POST.get("Digits", None)
        sid = request.POST.get("CallSid", None)
        obj_parent = ReservationParent.objects.get(sid=sid)
        
        if digit_pressed == "1":
            r_datetime   = obj_parent.reservation_datetime.astimezone(ZoneInfo(key='Asia/Tokyo'))
            r_year       = r_datetime.year
            r_month      = r_datetime.month
            r_day        = r_datetime.day
            r_hour       = r_datetime.hour
            r_minute     = r_datetime.minute
            r_num_people = obj_parent.num_people
            r_name       = obj_parent.representative_name
            n_datetime = datetime.datetime.now(ZoneInfo(key='Asia/Tokyo'))
            n_year = n_datetime.year
            n_month = n_datetime.month
            n_day = n_datetime.day

            message = "予約受付ありがとうございました。"

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

            message += f"{r_num_people}名、代表者名は、{r_name}でよろしくお願いします。"
            
            response = call_manager.create_say_response_xml(message)

            obj_child = ReservationChild.objects.create(
                parent     = obj_parent,
                status     = ReservationChild.SUCCESS,
                title_ja   = '予約受付が承認しました',
                title_en   = 'Reservation accepted and approved',
                message_ja = '店舗様が予約受付を承認しました。',
                message_en = 'Store has approved the reservation.',
            )

            obj_child = ReservationChild.objects.create(
                parent     = obj_parent,
                status     = ReservationChild.END,
                title_ja   = '代理予約が完了しました',
                title_en   = 'Proxy booking has been completed',
                message_ja = '代理予約処理が完了しました。',
                message_en = 'Proxy reservation processing has been completed.',
            )

            url = f"{'{0}://{1}'.format(self.request.scheme, self.request.get_host())}{reverse('main_app:reservation_detail', args=[obj_parent.id])}"

            UserNotice.objects.create(
                user=obj_parent.user,
                title_ja="予約受付が承認しました",
                title_en="Reservation accepted and approved",
                message_ja=f"店舗様が予約受付が承認しました。クリックすると、予約状況確認ページへリダイレクトします。",
                message_en=f"The store has approved the reservation receipt. Clicking on the button will redirect you to the reservation status confirmation page.",
                type=UserNotice.SUCCESS,
                url=url
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
                title_ja   = '予約受付が承認されませんでした',
                title_en   = 'Reservation not approved',
                message_ja = '店舗様が予約受付を承認しませんでした。',
                message_en = 'The store did not approve the reservation.',
            )

            obj_child = ReservationChild.objects.create(
                parent     = obj_parent,
                status     = ReservationChild.END,
                title_ja   = '代理予約が完了しました',
                title_en   = 'Proxy booking has been completed',
                message_ja = '代理予約処理が完了しました。',
                message_en = 'Proxy reservation processing has been completed.',
            )

            url = f"{'{0}://{1}'.format(self.request.scheme, self.request.get_host())}{reverse('main_app:reservation_detail', args=[obj_parent.id])}"

            UserNotice.objects.create(
                user=obj_parent.user,
                title_ja="予約受付が承認されませんでした",
                title_en="Reservation not approved",
                message_ja=f"店舗様が予約受付が承認しませんでした。クリックすると、予約状況確認ページへリダイレクトします。",
                message_en=f"The store did not approve the reservation receipt. Clicking on this button will redirect you to the reservation status confirmation page.",
                type=UserNotice.DANGER,
                url=url
            )

            obj_parent.is_end = True
            obj_parent.end_datetime = timezone.now()
            obj_parent.save()

        else:
            message = "こんにちは。本日の21時から3名で予約を取りたいのですが、可能でしょうか。予約可能の場合は1を、予約が不可能の場合は2を、この音声をもう1度聞く場合は3を押して下さい。"
            response = call_manager.create_gather_response_xml(message, next_url)

            obj_child = ReservationChild.objects.create(
                parent     = obj_parent,
                status     = ReservationChild.WAIT,
                title_ja   = '通話中',
                title_en   = "During a call",
                message_ja = 'ただいま通話中です。しばらくお待ちください。',
                message_en = "The call is in progress. Please wait a moment.",
            )
        

        return HttpResponse(response, content_type='text/xml')
