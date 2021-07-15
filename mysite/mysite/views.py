from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import FileResponse
from django.http import JsonResponse

import math
from geopy.geocoders import Nominatim



def getClosest(request, address):

    f = open("/home/nigel675/mysite/static/data/tennis courts dataset.json")
    data = json.load(f)
    n = []

    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(address)

    lat1 = location.latitude
    lon1 = location.longitude

    for i in data:

        lat2 =  i["coordArray"][0]
        lon2 = i["coordArray"][1]

        r = 6371000 # metres
        phi_one = lat1 * math.pi/180
        phi_two = lat2 * math.pi/180
        delta_phi = (lat2-lat1) * math.pi/180
        delta_lambda = (lon2-lon1) * math.pi/180

        a = math.sin(delta_phi/2) * math.sin(delta_phi/2) + math.cos(phi_one) * math.cos(phi_two) * math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        # r*c is in metres, convert to kilometers
        d = r*c

        i["Distance"] = round(d/ 1000,1)

        id_coord_arr = []
        id_coord_arr.append(round(d/ 1000,3))
        id_coord_arr.append(json.dumps(i))
        n.append(id_coord_arr)


    n.sort()
    new_list = []
    for q in n[:5:]:
        new_list.append(json.loads(q[1]))

    # x = "<html><body>%s</body></html>" % closest

    return JsonResponse(new_list, safe=False)

def find(request):
    return render(request, 'find.html')

def getLatLng(request,address):
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(address)

    lat = location.latitude
    lon = location.longitude

    return JsonResponse([lat,lon], safe=False)







