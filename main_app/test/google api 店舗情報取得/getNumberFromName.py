import googlemaps
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def get_phone_number(place_name, api_key):
    gmaps = googlemaps.Client(key=api_key)

    # 場所の検索
    places_result = gmaps.places(place_name)

    if places_result['status'] == 'OK':
        # 最初の結果の詳細を取得
        place_id = places_result['results'][0]['place_id']
        place_details = gmaps.place(place_id)

        # 電話番号を返す
        return place_details['result'].get('formatted_phone_number')

    return "該当する場所が見つかりませんでした。"


api_key = os.environ['GoogleAPI'] 
print(get_phone_number('マクドナルド与那原', api_key))