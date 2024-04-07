import googlemaps
from datetime import datetime
import matplotlib.pyplot as plt
import sys


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

    def get_coordinates(self, location_string):
        """
        Get the latitude and longitude for a given location string using the Google Maps Geocoding API.

        Parameters:
        - location_string: The string of the address or location to geocode.

        Returns:
        A tuple containing the latitude and longitude of the location.
        """
        geocode_result = self.gmaps.geocode(location_string)

        # Check if geocode results were found
        if geocode_result:
            latitude = geocode_result[0]["geometry"]["location"]["lat"]
            longitude = geocode_result[0]["geometry"]["location"]["lng"]
            return latitude, longitude
        else:
            raise ValueError(
                "Geocode API did not return a result for the specified location string."
            )

    def plot_nodes(self, locations, node_mapping, path=None):
        """
        Generate a plot view of the nodes with a comment on the node mapping.
        """
        try:
            plt.figure(figsize=(10, 10))

            # Plot each location
            for label, (lat, lon) in locations.items():
                plt.plot(lon, lat, "ro")  # 'ro': red circle markers
                plt.text(lon, lat, label, fontsize=12)  # add text labels to the markers

            # If a path is provided, plot lines between each consecutive pair of nodes
            if path:
                for i in range(len(path) - 1):
                    node_start = path[i]
                    node_end = path[i + 1]
                    start_coords = locations[node_start]
                    end_coords = locations[node_end]
                    plt.plot(
                        [start_coords[1], end_coords[1]],  # X coordinates: longitudes
                        [start_coords[0], end_coords[0]],  # Y coordinates: latitudes
                        "k-",  # 'k-' : black lines
                    )

            # set labels and title
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            plt.title("Ideal Route: Node Plot View")

            # adjust the subplot parameters: add space at the bottom
            plt.subplots_adjust(bottom=0.27)

            # comment below the plot for node mapping
            mapping_comment = "Node Mapping: \n" + "\n".join(
                f"{k}={v}" for k, v in node_mapping.items()
            )
            plt.figtext(0.5, 0.01, mapping_comment, ha="center", fontsize=11, wrap=True)

            plt.savefig("ideal_route.png", bbox_inches="tight")
        except Exception as e:
            print(f"An error occurred while plotting the nodes: {e}", file=sys.stderr)
