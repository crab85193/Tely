import os
from dotenv import load_dotenv
import requests
import googlemaps

load_dotenv()

class GooglePlacesAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.search_endpoint_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        self.details_endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        self.gmaps = googlemaps.Client(key=api_key)

    def get_exact_name(self, store_name):
        search_params = {
            'input': store_name,
            'inputtype': 'textquery',
            'fields': 'name',
            'key': self.api_key
        }

        response = requests.get(self.search_endpoint_url, params=search_params)
        if response.status_code == 200:
            results = response.json().get('candidates', [])
            if not results:
                return "No results found"
            return [(place['name']) for place in results]
        else:
            return f"Error: {response.status_code}"

    def get_store_number(self, place_id):
        params = {
            'place_id': place_id,
            'fields': 'name,rating,formatted_phone_number',
            'key': self.api_key
        }

        response = requests.get(self.details_endpoint_url, params=params)
        if response.status_code == 200:
            data = response.json()
            store_number = data['result'].get('formatted_phone_number')
            return store_number
        else:
            print("Error:", response.status_code)
            return None

    def get_phone_number(self, place_name):
        places_result = self.gmaps.places(place_name)
        if places_result['status'] == 'OK':
            place_id = places_result['results'][0]['place_id']
            place_details = self.gmaps.place(place_id)
            return place_details['result'].get('formatted_phone_number')
        return "No results found"

    def get_place_id(self, store_name):
        search_params = {
            'input': store_name,
            'inputtype': 'textquery',
            'fields': 'place_id,name',
            'key': self.api_key
        }

        response = requests.get(self.search_endpoint_url, params=search_params)
        if response.status_code == 200:
            results = response.json().get('candidates', [])
            if not results:
                return "No results found"
            return [(place['place_id']) for place in results]
        else:
            return f"Error: {response.status_code}"
        
    def get_store_address_by_name(self, store_name):
        place_id = self.get_place_id(store_name)
        if not place_id:
            return "店舗が見つかりません"

        params = {
            'place_id': place_id,
            'fields': 'formatted_address',
            'key': self.api_key,
            'language': 'ja'
        }

        response = requests.get(self.details_endpoint_url, params=params)
        if response.status_code == 200:
            data = response.json().get('result', {})
            return data.get('formatted_address', "住所が見つかりません")
        else:
            return f"エラー: {response.status_code}"
        
    
    def get_store_hours_by_name(self, store_name):
        place_id = self.get_place_id(store_name)
        if not place_id:
            return "店舗が見つかりません"

        params = {
            'place_id': place_id,
            'fields': 'opening_hours',
            'key': self.api_key,
            'language': 'ja'
        }

        response = requests.get(self.details_endpoint_url, params=params)
        if response.status_code == 200:
            data = response.json().get('result', {})
            return data.get('opening_hours', "営業時間情報が見つかりません")
        else:
            return f"エラー: {response.status_code}"
        
    def get_business_status(self, store_name):
        place_id = self.get_place_id(store_name)
        if not place_id:
            return "店舗が見つかりません"

        params = {
            'place_id': place_id,
            'fields': 'business_status',
            'key': self.api_key,
            'language': 'ja'
        }

        response = requests.get(self.details_endpoint_url, params=params)
        if response.status_code == 200:
            data = response.json().get('result', {})
            return data.get('business_status', "ビジネスステータスが見つかりません")
        else:
            return f"エラー: {response.status_code}"


# 使用例
api_key = os.environ['GoogleAPI']
google_places_api = GooglePlacesAPI(api_key)
store_name = 'マック与那原'
place_id = 'ChIJLceIYMMS5TQRPUNBaGw8Vo4'

# 店舗名を取得
exact_names = google_places_api.get_exact_name(store_name)
print(exact_names)

# プレイスidから電話番号を取得
store_number = google_places_api.get_store_number(place_id)
print(store_number)

# 店舗名から電話番号を取得
phone_number = google_places_api.get_phone_number(store_name)
print(phone_number)

# プレイスidを取得
place_ids = google_places_api.get_place_id(store_name)
print(place_ids)

# 住所を取得
address = google_places_api.get_store_address_by_name(store_name)
print("住所:", address)

# 営業時間を取得
hours = google_places_api.get_store_hours_by_name(store_name)
print("営業時間:", hours)

# ビジネスステータスを取得
business_status = google_places_api.get_business_status(store_name)
print("ビジネスステータス:", business_status)