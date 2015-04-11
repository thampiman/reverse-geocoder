Reverse Geocoder
-----------------
Reverse Geocoder takes a latitude / longitude coordinate and returns the nearest town/city.
This library improves on an existing library called reverse_geocode developed by Richard Penman in the following ways:
1. Besides city and country, this library also returns the administrative 1 & 2 regions, latitude and longitude
2. The performance is much faster since a parallelized K-D tree is implemeneted 
(See https://github.com/thampiman/reverse-geocoder for performance comparison)

Supports Python 2 and 3.

Example usage:
    >>> import reverse_geocoder as rg
    >>> coordinates = (51.5214588,-0.1729636),(9.936033, 76.259952),(37.38605,-122.08385)
    >>> rg.search(coordinates)
    [{'name': 'Bayswater', 
      'cc': 'GB', 
      'lat': '51.51116',
      'lon': '-0.18426', 
      'admin1': 'England', 
      'admin2': 'Greater London'}, 
     {'name': 'Cochin', 
      'cc': 'IN', 
      'lat': '9.93988',
      'lon': '76.26022', 
      'admin1': 'Kerala', 
      'admin2': 'Ernakulam'},
     {'name': 'Mountain View', 
      'cc': 'US', 
      'lat': '37.38605',
      'lon': '-122.08385', 
      'admin1': 'California', 
      'admin2': 'Santa Clara County'}]