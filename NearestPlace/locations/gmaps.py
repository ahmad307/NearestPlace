import googlemaps

class LocationFinder:
    def __init__(self):
        # Set gmaps api connection
        self.api = googlemaps.Client(key=open('D:/Projects/secretkey/gmaps_key.txt','r').read())

        # Temporary test locations
        self.user_places = [{'lat': 30.0185290, 'lng': 31.3261620}, {'lat': 30.099023, 'lng': 31.376186},
                   {'lat': 30.073690, 'lng': 31.285717}]

    def get_nearest_place(self,city,place_type):
        """Returns the nearest place to 'user_places' list.
        :param city: String with city in which to search for places.
        :param place_type: String with the kind of place sought.
        """
        place_location = self.get_location(city)
        result_places = self.get_places(place_type, place_location)

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
        """:param distances: dict returned from 'distance_matrix' method,
        with origin distances to destination.
        :returns: Total distance to be covered to reach destination.
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
            distances = self.api.distance_matrix(origins=self.user_places, destinations=place['geometry']['location'])

            total_distance = self.get_total_distance(distances)

            place_factor = total_distance / len(distances['rows'])
            destinations_factors.append((place_factor, place))

        return destinations_factors
