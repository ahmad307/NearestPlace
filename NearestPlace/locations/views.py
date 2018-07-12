from django.shortcuts import render, HttpResponse
from locations.gmaps import LocationFinder
from locations.models import Session
import json
import secrets
import string

def index(request):
    api_key = open('D:/Projects/secretkey/gmaps_key.txt','r').read()
    return render(request,'landing_page.html',{'api_key':api_key})

def get_location(request):
    """Receives POST request and returns the 'Nearest Place'."""
    if request.method == 'POST':
        city = request.POST.get('input_city')
        place_type = request.POST.get('input_placetype')

        location_finder = LocationFinder()
        result_place = location_finder.get_nearest_place(city, place_type)

        return HttpResponse(json.dumps({'place':result_place}), content_type='application/json')

def create_session(request):
    """Creates a session for saving locations in the database."""
    if request.method == 'POST':
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        print(code)
        session = Session(
            name = request.POST.get('meeting_name'),
            code = 'GFG9HE',
            place_type = request.POST.get('place_type'),
            city = request.POST.get('city')
        )
        session.save()
        return HttpResponse(json.dumps({'code':code}), content_type='application/json')