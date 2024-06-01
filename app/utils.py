from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic

key = 'dcde423f47e54054b1c9b36a74b2aa17'
geocoder = OpenCageGeocode(key)

def get_coordinates(address: str):
    key = 'dcde423f47e54054b1c9b36a74b2aa17'
    geocoder = OpenCageGeocode(key)
    results = geocoder.geocode(address)
    
    if results and len(results) > 0:
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        return lat, lng
    else:
        return None, None

def calculate_distance(coords1, coords2):
    if coords1 and coords2:
        return geodesic(coords1, coords2).meters
    return None


