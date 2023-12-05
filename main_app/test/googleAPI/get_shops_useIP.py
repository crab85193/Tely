import os
from dotenv import load_dotenv
import googlemaps
import geocoder
load_dotenv()
key = os.environ['GoogleAPI']

gmaps = googlemaps.Client(key)
location = geocoder.ip('me').latlng
places_result = gmaps.places_nearby(location=location, keyword='マクドナルド', radius=50000, language="ja")

for place in places_result['results']:
    print(place['name'])
    