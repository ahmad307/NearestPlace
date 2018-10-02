from locations.models import Session,Location
import googlemaps

class LocationFinder:
    def __init__(self,meeting):
        """:param meeting: Session table object for which to get Nearest Place."""
        # Set gmaps api connection
        self.api = googlemaps.Client(key=open('D:/Projects/secretkey/gmaps_key.txt','r').read())

        # Get locations of users in the meeting
        locations = Location.objects.filter(session=meeting)    # List of all locations related to meeting
        self.users_places = [{'lat': i.latitude, 'lng': i.longitude} for i in locations]

        # Get meeting's info
        self.city = meeting.city    # City in which to search for places.
        self.place_type = meeting.place_type    # The kind of place sought.

    def get_nearest_place(self):
        """Returns the nearest place to 'users_places' list."""
        place_location = self.get_location(self.city)
        result_places = self.get_places(self.place_type, place_location)

        factors = self.get_places_factors(result_places)
        factors.sort(key=lambda tup: tup[0])

        return factors[0][1]['name']

    def get_location(self,address):
        """Returns location dict with lat and lng
        :param address: string with city/area name
        """
        # Get area/city coordinates
        place = self.api.geocode(address=address)
        return place[0]['geometry']['location']

    def get_places(self,place_type, area):
        # Return a list of spots near 'area'
        return self.api.places(query=place_type, location=area)

    def get_total_distance(self,distances):
        """Returns total distance to be covered to reach destination.
        :param distances: dict returned from 'distance_matrix' method,
        with origin distances to destination.
        """
        total_distance = 0
        # Iterate over each distance to destination
        for distance in distances['rows']:
            total_distance += int(distance['elements'][0]['distance']['value']) / 1000

        return total_distance

    def get_places_factors(self,result_places):
        """Returns a list of total average distance for each given place.
        :param result_places: dict with list of places found in search
        """
        # Calculate distance factor for each potential place
        destinations_factors = []
        for place in result_places['results']:
            # Get each distance to destination using their location
            distances = self.api.distance_matrix(origins=self.users_places, destinations=place['geometry']['location'])

            total_distance = self.get_total_distance(distances)

            place_factor = total_distance / len(distances['rows'])
            destinations_factors.append((place_factor, place))

        return destinations_factors
