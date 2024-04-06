import googlemaps
from datetime import datetime


class GoogleMapsUtil:
    def __init__(self, api_key):
        self.gmaps = googlemaps.Client(key=api_key)  # Removed the stray 'self'

    def calculate_distance(self, origin, destination, mode="driving"):
        """Calculate the distance between two locations using the Google Maps API."""
        now = datetime.now()
        directions_result = self.gmaps.directions(
            origin, destination, mode=mode, departure_time=now
        )

        # Check if results were found and extract distance
        if directions_result and "legs" in directions_result[0]:
            distance_meters = directions_result[0]["legs"][0]["distance"]["value"]
            distance_miles = distance_meters / 1609.34  # Convert meters to miles
            return round(distance_miles, 2)
        else:
            raise ValueError(
                "No directions could be found between the specified locations."
            )
