from django.shortcuts import render
from locations.gmaps import LocationFinder

def index(request):
    api_key = open('D:/Projects/secretkey/gmaps_key.txt','r').read()
    result_place = ""
    if request.method == 'POST':
        city = request.POST.get('input_city')
        place_type = request.POST.get('input_placetype')

        location_finder = LocationFinder()
        result_place = location_finder.get_nearest_place(city,place_type)

    return render(request,'landing_page.html',{'result_place':result_place,'api_key':api_key})
