Reverse Geocoder
-----------------
Reverse Geocoder takes a latitude / longitude coordinate and returns the nearest town/city.
This library improves on an existing library called reverse_geocode developed by Richard Penman in the following ways:
1. Besides city and country, this library also returns the administrative 1 & 2 regions, latitude and longitude
2. The performance is much faster since a parallelized K-D tree is implemeneted 
(See https://github.com/thampiman/reverse-geocoder for performance comparison)

Example usage:
    >>> import reverse_geocoder as rg
    >>> coordinates = (51.5214588,-0.1729636),(13.9280531,100.3735803)
    >>> rg.search(coordinates)
    [{'admin1': 'England',
  	  'admin2': 'Greater London',
  	  'cc': 'GB',
  	  'lat': '51.51116',
  	  'lon': '-0.18426',
  	  'name': 'Bayswater'},
 	 {'admin1': 'Nonthaburi',
  	  'admin2': '',
  	  'cc': 'TH',
  	  'lat': '13.91783',
  	  'lon': '100.42403',
  	  'name': 'Bang Bua Thong'}]
