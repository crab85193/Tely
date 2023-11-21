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


# 使用例
api_key = os.environ['GoogleAPI']
google_places_api = GooglePlacesAPI(api_key)

store_name = 'マック与那原'
exact_names = google_places_api.get_exact_name(store_name)
print(exact_names)

place_id = 'ChIJLceIYMMS5TQRPUNBaGw8Vo4'
store_number = google_places_api.get_store_number(place_id)
print(store_number)

place_name = 'マクドナルド与那原'
phone_number = google_places_api.get_phone_number(place_name)
print(phone_number)

place_ids = google_places_api.get_place_id(store_name)
print(place_ids)
