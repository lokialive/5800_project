import requests
import random
import math

class AddressGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_location(self, address):
        # transfer the location to Longitude and Latitude
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={self.api_key}"
        response = requests.get(geocode_url)
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        return None, None

    def generate_random_points(self, lat, lng, radius_km, count):
        # generate random location, the count is random number between [2, 10]
        random_points = []
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            r = radius_km * math.sqrt(random.uniform(0, 1))
            delta_lat = r / 110.574
            delta_lng = r / (111.320 * math.cos(math.radians(lat)))
            random_lat = lat + delta_lat * math.cos(angle)
            random_lng = lng + delta_lng * math.sin(angle)
            random_points.append((random_lat, random_lng))
        return random_points

    def get_address(self, lat, lng):
        # get location
        reverse_geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={self.api_key}"
        response = requests.get(reverse_geocode_url)
        data = response.json()
        if data['results']:
            return data['results'][0]['formatted_address']
        return "Unknown location"
