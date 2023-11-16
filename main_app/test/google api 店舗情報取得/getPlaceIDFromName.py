import os
from dotenv import load_dotenv
import requests

load_dotenv()

def get_place_id(store_name, api_key):
    search_endpoint_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

    # 検索用のパラメータ
    search_params = {
    'input': store_name,
    'inputtype': 'textquery',
    'fields': 'place_id,name',
    'key': api_key
    }

    # Google Places APIへリクエストを送る
    response = requests.get(search_endpoint_url, params=search_params)
    if response.status_code == 200:
        # レスポンスJSONを解析
        results = response.json().get('candidates', [])
        if not results:
            return "No results found"
        return [(place['place_id']) for place in results]
    else:
        return f"Error: {response.status_code}"


    
api_key = os.environ['GoogleAPI']  
store_name = 'マック与那原' #多少違っても予測変換した結果を検索してくれる

place_ids = get_place_id(store_name, api_key)
print(place_ids)

