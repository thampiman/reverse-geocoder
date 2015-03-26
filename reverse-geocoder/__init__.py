import os
import sys
import csv
csv.field_size_limit(sys.maxint)
import urllib
import zipfile
import collections
from scipy.spatial import cKDTree as KDTree

GN_URL = 'http://download.geonames.org/export/dump/'
GN_CITIES1000 = 'cities1000'
GN_ADMIN1 = 'admin1CodesASCII'
GN_ADMIN2 = 'admin2Codes'

# Columns from GN_URL
GN_COLUMNS = [
  'geoNameId', 
  'name', 
  'asciiName',
  'alternateNames', 
  'latitude', 
  'longitude', 
  'featureClass',
  'featureCode',
  'countryCode',
  'cc2', 
  'admin1Code',
  'admin2Code', 
  'admin3Code', 
  'admin4Code', 
  'population', 
  'elevation', 
  'dem', 
  'timezone', 
  'modificationDate', 
]

RG_COLUMNS = [
    'latitude',
    'longitude',
    'name',
    'admin1',
    'admin2',
    'country_code'
]

RG_FILE = 'rg_cities1000.csv'

def singleton(cls):
    # Singleton pattern to avoid loading class multiple times
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class RGeocoder:
    def __init__(self):
        coordinates, self.locations = self.extract(rel_path(geocode_filename))
        self.tree = KDTree(coordinates)


def rel_path(filename):
    # Return the path of this filename relative to the current script
    return os.path.join(os.getcwd(), os.path.dirname(__file__), filename)

def get(coordinate):
    # Search for closest known location to this coordinate
    rg = RGeocoder()
    return rg.query([coordinate])[0]

def search(coordinates):
    # Search for closest known locations to these coordinates
    rg = RGeocoder()
    return rg.query(coordinates)