from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from urllib.parse import urlencode
from ..models.notice import Notice
from ..models.reservation import ReservationParent,ReservationChild
from ..models.store import Store
from ..store_manager import StoreManager

class TopView(LoginRequiredMixin, TemplateView):
    template_name = 'main_app/index.html'
    
    def get_context_data(self, **kwargs):
        store_manager = StoreManager()
        context = super().get_context_data(**kwargs)
        
        context["notices"] = Notice.objects.order_by('-datetime').all()[:3]
        reservation_parent = ReservationParent.objects.filter(user=self.request.user).order_by("-start_datetime").first()
        if reservation_parent:
            context["reservation_title"] = reservation_parent.shop_name
            context["reservation_id"] = reservation_parent.id
            context["reservation_detail_items"] = ReservationChild.objects.filter(parent=reservation_parent).order_by("datetime")

        stores_info = []
        store_info_inner = []

        for store in Store.objects.filter(archive=False):
            store_info = {}
            store_info["place_id"] = store.place_id
            store_info["name"] = store.name

            store_types = ""
            for type in store.type.split(" "):
                match type:
                    case "bakery":
                        store_types += "パン屋" + ", "
                    case "bar":
                        store_types += "バー" + ", "
                    case "cafe":
                        store_types += "カフェ" + ", "
                    case "convenience_store":
                        store_types += "コンビニ" + ", "
                    case "food":
                        store_types += "飲食店" + ", "
                    case "restaurant":
                        store_types += "レストラン" + ", "
                    case _:
                        pass
                    
            store_info["type"] = store_types
            store_info["open"] = store.open
            store_info["photo"] = store.photo_url
            store_info["rating"] = store.rating
            store_info["price_level"] = store.price_level
            store_info["record_datetime"] = store.record_datetime
            store_info["add_url"] = f"{reverse('main_app:reservation_add')}?{urlencode({'place_id': store_info['place_id']})}"
            store_info["detail_url"] = f"{reverse('main_app:shop_detail')}?{urlencode({'place_id': store_info['place_id']})}"
            store_info_inner.append(store_info)
            print(store_info_inner)

            if len(store_info_inner) == 2:
                stores_info.append(store_info_inner)
                store_info_inner = []

        if len(store_info_inner) >= 1:
            stores_info.append(store_info_inner)

        context["stores_info"] = stores_info

        # histories_info = []
        # history_info_inner = []

        # for history in ReservationParent.objects.all().filter(user=self.request.user).order_by("-start_datetime"):
        #     history_info = {} 

        
        # context["histories"] 

        return context