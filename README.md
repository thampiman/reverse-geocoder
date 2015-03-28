Reverse Geocoder
=================
A Python library for offline reverse geocoding. It improves on an existing library called [reverse_geocode](https://pypi.python.org/pypi/reverse_geocode/1.0) developed by [Richard Penman](https://bitbucket.org/richardpenman/reverse_geocode).

*Update*: v1.1 released! Python 3 not supported still.

### About
Ajay Thampi | [@thampiman](https://twitter.com/thampiman) | [opensignal.com](http://opensignal.com) | [ajaythampi.com](http://ajaythampi.com)

## Features
1. Besides city/town and country code, this library also returns the nearest latitude and longitude and also administrative regions 1 and 2.
2. This library also uses a parallelised implementation of K-D trees which promises an improved performance especially for large inputs.

The K-D tree is populated with cities that have a population > 1000. The source of the data is [GeoNames](http://download.geonames.org/export/dump/).

## Installation
```
$ pip install reverse_geocoder
```

Package can be found on [PyPI](https://pypi.python.org/pypi/reverse_geocoder/).

*Update*: v1.1 released containing [Brandon](https://github.com/bdon)'s and [David](https://github.com/DavidJFelix)'s fixes

## Usage
The library supports two modes:

1. Mode 1: Single-threaded K-D Tree (similar to [reverse_geocode](https://pypi.python.org/pypi/reverse_geocode/1.0))
2. Mode 2: Multi-threaded K-D Tree (default)

```python
import reverse_geocoder as rg

coordinates = (51.5214588,-0.1729636),(13.9280531,100.3735803)

results = rg.search(coordinates) # default mode = 2

print results
```

The above code will output the following:
```
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
```

If you'd like to use the single-threaded K-D tree, set mode = 1 as follows:
```python
results = rg.search(coordinates,mode=1)
```

## Performance
The performance of modes 1 and 2 are plotted below for various input sizes.

![Performance Comparison](performance.png)

Mode 2 runs ~2x faster for very large inputs (10M coordinates).

## Acknowledgements
1. Major inspiration is from Richard Penman's [reverse_geocode](https://bitbucket.org/richardpenman/reverse_geocode) library 
2. Parallelised implementation of K-D Trees is extended from this [article](http://folk.uio.no/sturlamo/python/multiprocessing-tutorial.pdf) by [Sturla Molden](https://github.com/sturlamolden)
3. Geocoded data is from [GeoNames](http://download.geonames.org/export/dump/)

## License
The MIT License (MIT)