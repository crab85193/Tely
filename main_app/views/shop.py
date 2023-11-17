from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ShopListView(LoginRequiredMixin, TemplateView):
    template_name = 'main_app/shop/shop_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        shop_list = []

        shop_detail1 = {
            "img":"https://night-planet.s3.ap-northeast-1.amazonaws.com/shops/b3cb55c646e4c2df012ddb4df60d31f680ea7c1f/top_image/b3cb55c646e4c2df012ddb4df60d31f680ea7c1f.jpg",
            "name":"ガールズバー Macherie(マシェリ)",
            "type":"ガールズバー",
            "address":"沖縄県与那原町与那原3178-3",
            "tel_number":"080-4289-7797",
            "open":"月〜土 9:00〜Last",
            "closed":"日曜日",
            "detail":"🥂 𝟼𝟶𝚖𝚒𝚗 ¥𝟹𝟶𝟶𝟶\n最新カラオケ🎤ダーツ🎯完備\nオリオン通りを入って徒歩2分"
        }

        shop_list.append(shop_detail1)

        context["shop_list"] = shop_list

        return context


class ShopDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'main_app/shop/shop_detail.html'

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