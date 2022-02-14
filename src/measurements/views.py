from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo

# Create your views here.

def calculate_distance_view(request):
    obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurements')
    
    ip = '207.126.159.255'
    country, city, lat, lon = get_geo(ip)
    #print('location country', country)
    #print('location city', city)
    #print('location lat, lon', lat, lon)
    
    location = geolocator.geocode(city)
    #print('###', location)

    # Define distance between the 2 points
    loc_lat = lat
    loc_lon = lon
    startPoint = (lat, lon)
    
    
    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)
        #print(destination)
        dest_lat = destination.latitude
        dest_long = destination.longitude
        
        finishPoint = (dest_lat, dest_long)
        totalDistance = round(geodesic(startPoint, finishPoint).km, 2)
        
        instance.location = location
        instance.distance = totalDistance
        instance.save()
    
    context = {
      'distance' : obj,
      'form' : form,
    }
    
    return render(request, 'measurements/main.html', context)
