from django.shortcuts import render, HttpResponse
from locations.gmaps import LocationFinder
from django.core.exceptions import ValidationError
from locations.models import Session,Location
import json
import secrets
import string
from decimal import *

def index(request):
    api_key = open('D:/Projects/secretkey/gmaps_key.txt','r').read()
    return render(request,'landing_page.html',{'api_key':api_key})

def meeting(request):
    return render(request,'meeting.html')

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
        # Create pseudo-unique random string of numbers and capital letters
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))

        session = Session(
            name = request.POST.get('meeting_name'),
            code = code,
            place_type = request.POST.get('place_type'),
            city = request.POST.get('city')
        )

        # Validate data before saving to Database
        try:
            session.full_clean()
            session.save()
        except ValidationError:
            print('ValidaionError!')
            return HttpResponse(json.dumps({'message':'ValidationError'}), content_type='application/json')

        return HttpResponse(json.dumps({'message':'success','code':code}), content_type='application/json')

def add_location(request):
    """Adds a new location to the given meeting and saves it in DB."""
    if request.POST:
        # Get request data
        code = request.POST.get('code')
        lat = round(Decimal(request.POST.get('lat')),6)
        lng = round(Decimal(request.POST.get('lng')),6)

        # Create object of location with the given Session's code
        session = Session.objects.get(code=code)
        location = Location(
            longitude=lng,
            latitude=lat,
            session=session
        )

        # Validate data before saving to Database
        try:
            location.full_clean()
            location.save()
            print('location saved!')
            result = {'message':'Success'}
        except ValidationError as e:
            print(e)
            result = {'message':'Validaiton Error'}

        return HttpResponse(json.dumps(result), content_type='application/json')
