from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..store_manager import StoreManager
from urllib.parse import urlencode
from django.utils.translation import gettext_lazy as _

class ShopListView(LoginRequiredMixin, TemplateView):
    template_name = 'main_app/shop/shop_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store_manager = StoreManager()
        shop_list = []

        if self.request.GET.get("keywords"):
            keywords = self.request.GET.get("keywords")
            context["keywords"] = keywords
            search_results = store_manager.search_store(keywords)
        else:
            shop_detail_test = {
                "img":"https://raw.githubusercontent.com/crab85193/Tely/main/static/img/logo.png",
                "name":"テスト用店舗 001店",
                "type":"レストラン",
                "address":"沖縄県中頭郡西原町字千原",
                "tel_number":"090-5516-9212",
                "open":"月〜土 9:00〜Last",
                "detail_url": f"{reverse('main_app:shop_detail')}",
                "add_url": f"{reverse('main_app:reservation_add')}",
                "rating":float("3.0"),
                "test":True,
            }

            shop_list.append(shop_detail_test)

            search_results = store_manager.search_store("飲食店")

        for store_info in search_results:
            detail = {}

            detail["place_id"] = store_info["place_id"]
            detail["name"] = store_info["name"]

            store_types = ""
            for type in store_info["type"]:
                match type:
                    case "bakery":
                        store_types += _("bakery") + ", "
                    case "bar":
                        store_types += _("bar") + ", "
                    case "cafe":
                        store_types += _("cafe") + ", "
                    case "convenience_store":
                        store_types += _("convenience_store") + ", "
                    case "food":
                        store_types += _("food") + ", "
                    case "restaurant":
                        store_types += _("restaurant") + ", "
                    case _:
                        pass
            detail["type"] = store_types

            detail["open"] = store_info["open"]
            
            if store_info["photos"]:
                detail["img"] = store_info["photos"]
            else:
                detail["img"] = None

            detail["rating"] = float(store_info["rating"])
            detail["price_level"] = store_info["price_level"]
            detail["detail_url"] = f"{reverse('main_app:shop_detail')}?{urlencode({'place_id': store_info['place_id']})}"
            detail["add_url"] = f"{reverse('main_app:reservation_add')}?{urlencode({'place_id': store_info['place_id']})}"

            shop_list.append(detail)

        context["shop_list"] = shop_list

        return context


class ShopDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'main_app/shop/shop_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store_manager = StoreManager()

        if self.request.GET.get("place_id"):
            store_info = store_manager.get_store_detail(self.request.GET.get("place_id"))
            shop_detail = {}
            
            shop_detail["img_list"] = store_info["photos"]
            shop_detail["name"] = store_info["name"]
            shop_detail["address"] = store_info["address"]
            shop_detail["tel_number"] = store_info["tel_number"]
            shop_detail["add_url"] = f"{reverse('main_app:reservation_add')}?{urlencode({'place_id': store_info['place_id']})}"
            
            store_types = ""
            for type in store_info["type"]:
                match type:
                    case "bakery":
                        store_types += _("bakery") + ", "
                    case "bar":
                        store_types += _("bar") + ", "
                    case "cafe":
                        store_types += _("cafe") + ", "
                    case "convenience_store":
                        store_types += _("convenience_store") + ", "
                    case "food":
                        store_types += _("food") + ", "
                    case "restaurant":
                        store_types += _("restaurant") + ", "
                    case _:
                        pass
            shop_detail["type"] = store_types

            shop_detail["open"] = ""
            for hours in store_info["open"]:
                shop_detail["open"] += hours + "\n"

        else:
            shop_detail = {
                "img_list":[
                    "https://raw.githubusercontent.com/crab85193/Tely/main/static/img/logo.png"
                    ],
                "name":"テスト用店舗 001店",
                "type":"レストラン",
                "address":"沖縄県中頭郡西原町字千原",
                "tel_number":"090-5516-9212",
                "open":"月〜土 9:00〜Last",
                "add_url":f"{reverse('main_app:reservation_add')}",
                "test": True,
            }

        context["shop"] = shop_detail

        return context