import os
from dotenv import load_dotenv
import requests

# .envファイルの内容を読み込見込む
load_dotenv()


def get_store_number(place_id, api_key):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"

   
    params = {
        'place_id': place_id,
        'fields': 'name,rating,formatted_phone_number',
        'key': api_key
    }

    # Google Places APIへリクエストを送る
    response = requests.get(endpoint_url, params=params)
    if response.status_code == 200:
      
        data = response.json()
        
        store_number = data['result'].get('formatted_phone_number')
        return store_number
    else:
        print("Error:", response.status_code)
        return None
    

api_key = os.environ['GoogleAPI'] 
place_id = 'ChIJLceIYMMS5TQRPUNBaGw8Vo4'  
store_number = get_store_number(place_id, api_key)
print(store_number)