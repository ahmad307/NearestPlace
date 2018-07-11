from django.shortcuts import render, HttpResponse
from locations.gmaps import LocationFinder
import json

def index(request):
    api_key = open('D:/Projects/secretkey/gmaps_key.txt','r').read()
    return render(request,'landing_page.html',{'api_key':api_key})

def get_location(request):
    """Receives POST request and returns the 'Nearest Place'"""
    if request.method == 'POST':
        city = request.POST.get('input_city')
        place_type = request.POST.get('input_placetype')

        location_finder = LocationFinder()
        result_place = location_finder.get_nearest_place(city, place_type)

        return HttpResponse(json.dumps({'place':result_place}), content_type='application/json')
