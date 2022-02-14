from django.contrib.gis.geoip2 import GeoIP2

# Here is where we'll keep all the helper functions.


def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon