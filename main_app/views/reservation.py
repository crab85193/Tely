from django.views.generic import TemplateView, ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from ..call_manager import CallManager
from ..models.user import User
from ..models.reservation import ReservationParent, ReservationChild
from ..forms.reservation import ReservationForm


class ReservationPhoneView(LoginRequiredMixin, TemplateView):
    template_name = "main_app/reservation/reservation_phone.html"

    def post(self, request):
        call_manager = CallManager()
        call_manager.call("こんにちは。私は予約がしたい", request.POST['tel'])
        
        return HttpResponseRedirect(reverse('main_app:reservation_done')) 


class ReservationAddView(LoginRequiredMixin, FormView):
    template_name = 'main_app/reservation/reservation_add.html'
    form_class    = ReservationForm
    # success_url   = reverse_lazy('main_app:twilio_gather')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        shop_detail1 = {
            "img_list":[
                "https://night-planet.s3.ap-northeast-1.amazonaws.com/shops/b3cb55c646e4c2df012ddb4df60d31f680ea7c1f/top_image/b3cb55c646e4c2df012ddb4df60d31f680ea7c1f.jpg",
                "https://www.s-cheers.com/file/image/201712/53eed35318e89e643d1f7780884c7700.jpg",
                "https://night-planet.s3.ap-northeast-1.amazonaws.com/shops/b3cb55c646e4c2df012ddb4df60d31f680ea7c1f/image/09efce7ff1d925b43a3f051fe25b72b425707c3c.jpg"
                ],
            "name":"ガールズバー Macherie(マシェリ)",
            "type":"ガールズバー",
            "address":"沖縄県与那原町与那原3178-3",
            "tel_number":"080-4289-7797",
            "open":"月〜土 9:00〜Last",
            "closed":"日曜日",
            "detail":"🥂 𝟼𝟶𝚖𝚒𝚗 ¥𝟹𝟶𝟶𝟶\n最新カラオケ🎤ダーツ🎯完備\nオリオン通りを入って徒歩2分"
        }

        context["shop"] = shop_detail1

        return context

    def form_valid(self, form):
        data = form.cleaned_data

        obj_parent = ReservationParent.objects.create(
            user = self.request.user,
            shop_tel_number = "08042897797",
            shop_name = "ガールズバー Macherie(マシェリ)",
            reservation_datetime = data["reservation_datetime"],
            num_people = data["num_people"],
            representative_name = data["representative_name"],
            memo = data["memo"]
        )

        obj_child = ReservationChild.objects.create(
            parent=obj_parent,
            status=ReservationChild.START,
            title="代理予約を受け付けました",
            message="店舗様に電話を発信中です。しばらくお待ちください。"
        )
        
        return super().form_valid(form)

    def get_success_url(self):
        obj = ReservationParent.objects.all().order_by('-start_datetime').first()

        return reverse_lazy('main_app:twilio_gather', args=[obj.id])
    

class ReservationDoneView(LoginRequiredMixin, TemplateView):
    template_name = "main_app/reservation/reservation_done.html"


class ReservationListView(LoginRequiredMixin, TemplateView):
    template_name = "main_app/reservation/reservation_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"]    = ReservationParent.objects.filter(user=self.request.user).order_by("-start_datetime")
        context["incomplete"] = ReservationParent.objects.filter(user=self.request.user, is_end=False).order_by("-start_datetime")
        context["complete"]   = ReservationParent.objects.filter(user=self.request.user, is_end=True).order_by("-start_datetime")

        return context


class ReservationDetailView(LoginRequiredMixin, DetailView):
    template_name = "main_app/reservation/reservation_detail.html"
    model = ReservationParent
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        shop_detail1 = {
            "img_list":[
                "https://night-planet.s3.ap-northeast-1.amazonaws.com/shops/b3cb55c646e4c2df012ddb4df60d31f680ea7c1f/top_image/b3cb55c646e4c2df012ddb4df60d31f680ea7c1f.jpg",
                "https://www.s-cheers.com/file/image/201712/53eed35318e89e643d1f7780884c7700.jpg",
                "https://night-planet.s3.ap-northeast-1.amazonaws.com/shops/b3cb55c646e4c2df012ddb4df60d31f680ea7c1f/image/09efce7ff1d925b43a3f051fe25b72b425707c3c.jpg"
                ],
            "name":"ガールズバー Macherie(マシェリ)",
            "type":"ガールズバー",
            "address":"沖縄県与那原町与那原3178-3",
            "tel_number":"080-4289-7797",
            "open":"月〜土 9:00〜Last",
            "closed":"日曜日",
            "detail":"🥂 𝟼𝟶𝚖𝚒𝚗 ¥𝟹𝟶𝟶𝟶\n最新カラオケ🎤ダーツ🎯完備\nオリオン通りを入って徒歩2分"
        }

        context["shop"] = shop_detail1

        obj_parent = ReservationParent.objects.get(id=self.kwargs['pk'])
        obj_child = ReservationChild.objects.filter(parent=obj_parent).order_by("datetime")

        context["status"] = obj_child

        return context
