from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..store_manager import StoreManager
from urllib.parse import urlencode

class ShopListView(LoginRequiredMixin, TemplateView):
    template_name = 'main_app/shop/shop_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store_manager = StoreManager()

        shop_list = []

        shop_detail_test = {
            "img":"https://night-planet.s3.ap-northeast-1.amazonaws.com/shops/b3cb55c646e4c2df012ddb4df60d31f680ea7c1f/top_image/b3cb55c646e4c2df012ddb4df60d31f680ea7c1f.jpg",
            "name":"ガールズバー Macherie(マシェリ)",
            "type":"ガールズバー",
            "address":"沖縄県与那原町与那原3178-3",
            "tel_number":"080-4289-7797",
            "open":"月〜土 9:00〜Last",
            "detail_url": f"{reverse('main_app:shop_detail')}",
            "add_url": f"{reverse('main_app:reservation_add')}",
        }

        shop_list.append(shop_detail_test)

        search_results = store_manager.search_store("飲食店")

        for store_info in search_results:
            detail = {}

            detail["place_id"] = store_info["place_id"]
            detail["img"] = store_info["photos"]
            detail["name"] = store_info["name"]
            detail["address"] = store_info["address"]
            detail["tel_number"] = store_info["tel_number"]
            detail["detail_url"] = f"{reverse('main_app:shop_detail')}?{urlencode({'place_id': store_info['place_id']})}"
            detail["add_url"] = f"{reverse('main_app:reservation_add')}?{urlencode({'place_id': store_info['place_id']})}"

            store_types = ""
            for type in store_info["type"]:
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
            detail["type"] = store_types

            detail["open"] = ""
            for hours in store_info["open"]:
                detail["open"] += hours + "\n"

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
            shop_detail["type"] = store_types

            shop_detail["open"] = ""
            for hours in store_info["open"]:
                shop_detail["open"] += hours + "\n"

        else:
            shop_detail = {
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
                "add_url":f"{reverse('main_app:reservation_add')}"
            }

        context["shop"] = shop_detail

        return context