##
# Author: Ajay Thampi
##
from __future__ import print_function
import os
import sys
import csv
csv.field_size_limit(sys.maxsize)
import zipfile
from scipy.spatial import cKDTree as KDTree
from reverse_geocoder import cKDTree_MP as KDTree_MP
import numpy as np

GN_URL = 'http://download.geonames.org/export/dump/'
GN_CITIES1000 = 'cities1000'
GN_ADMIN1 = 'admin1CodesASCII.txt'
GN_ADMIN2 = 'admin2Codes.txt'

GN_COLUMNS = {
    'geoNameId': 0, 
    'name': 1, 
    'asciiName': 2,
    'alternateNames': 3, 
    'latitude': 4, 
    'longitude': 5, 
    'featureClass': 6,
    'featureCode': 7,
    'countryCode': 8,
    'cc2': 9, 
    'admin1Code': 10,
    'admin2Code': 11, 
    'admin3Code': 12, 
    'admin4Code': 13, 
    'population': 14, 
    'elevation': 15, 
    'dem': 16, 
    'timezone': 17, 
    'modificationDate': 18
}

ADMIN_COLUMNS = {
    'concatCodes': 0,
    'name': 1,
    'asciiName': 2,
    'geoNameId': 3   
}

RG_COLUMNS = [
    'lat',
    'lon',
    'name',
    'admin1',
    'admin2',
    'cc'
]

RG_FILE = 'rg_cities1000.csv'

A = 6378.137 # major axis in kms
E2 = 0.00669437999014

def singleton(cls):
    instances = {}
    def getinstance(mode=2,verbose=True):
        if cls not in instances:
            instances[cls] = cls(mode=mode,verbose=verbose)
        return instances[cls]
    return getinstance

@singleton
class RGeocoder:
    def __init__(self,mode=2,verbose=True):
        self.mode = mode
        self.verbose = verbose
        coordinates, self.locations = self.extract(rel_path(RG_FILE))
        if mode == 1: # Single-process
            self.tree = KDTree(coordinates)
        else: # Multi-process
            self.tree = KDTree_MP.cKDTree_MP(coordinates)
        

    def query(self,coordinates):
        try:
            if self.mode == 1:
                distances,indices = self.tree.query(coordinates,k=1)
            else:
                distances,indices = self.tree.pquery(coordinates,k=1)
        except ValueError as e:
            raise e
        else:
            return [self.locations[index] for index in indices]

    def extract(self,local_filename):
        if os.path.exists(local_filename):
            if self.verbose:
                print('Loading formatted geocoded file...')
            rows = csv.DictReader(open(local_filename,'rt'))
        else:
            gn_cities1000_url = GN_URL + GN_CITIES1000 + '.zip'
            gn_admin1_url = GN_URL + GN_ADMIN1
            gn_admin2_url = GN_URL + GN_ADMIN2

            cities1000_zipfilename = GN_CITIES1000 + '.zip'
            cities1000_filename = GN_CITIES1000 + '.txt'

            if not os.path.exists(cities1000_zipfilename):
                if self.verbose:
                    print('Downloading files from Geoname...')
                try: # Python 3
                    import urllib.request
                    urllib.request.urlretrieve(gn_cities1000_url,cities1000_zipfilename)
                    urllib.request.urlretrieve(gn_admin1_url,GN_ADMIN1)
                    urllib.request.urlretrieve(gn_admin2_url,GN_ADMIN2)
                except ImportError: # Python 2
                    import urllib
                    urllib.urlretrieve(gn_cities1000_url,cities1000_zipfilename)
                    urllib.urlretrieve(gn_admin1_url,GN_ADMIN1)
                    urllib.urlretrieve(gn_admin2_url,GN_ADMIN2)


            if self.verbose:
                print('Extracting cities1000...')
            z = zipfile.ZipFile(open(cities1000_zipfilename,'rb'))
            open(cities1000_filename,'wb').write(z.read(cities1000_filename))

            if self.verbose:
                print('Loading admin1 codes...')
            admin1_map = {}
            t_rows = csv.reader(open(GN_ADMIN1,'rt'),delimiter='\t')
            for row in t_rows:
                admin1_map[row[ADMIN_COLUMNS['concatCodes']]] = row[ADMIN_COLUMNS['asciiName']]

            if self.verbose:
                print('Loading admin2 codes...')
            admin2_map = {}
            for row in csv.reader(open(GN_ADMIN2,'rt'),delimiter='\t'):
                admin2_map[row[ADMIN_COLUMNS['concatCodes']]] = row[ADMIN_COLUMNS['asciiName']]

            if self.verbose:
                print('Creating formatted geocoded file...')
            writer = csv.DictWriter(open(local_filename,'wt'),fieldnames=RG_COLUMNS)
            rows = []
            for row in csv.reader(open(cities1000_filename,'rt'),delimiter='\t',quoting=csv.QUOTE_NONE):
                lat = row[GN_COLUMNS['latitude']]
                lon = row[GN_COLUMNS['longitude']]
                name = row[GN_COLUMNS['asciiName']]
                cc = row[GN_COLUMNS['countryCode']]

                admin1_c = row[GN_COLUMNS['admin1Code']]
                admin2_c = row[GN_COLUMNS['admin2Code']]

                cc_admin1 = cc+'.'+admin1_c
                cc_admin2 = cc+'.'+admin1_c+'.'+admin2_c

                admin1 = ''
                admin2 = ''

                if cc_admin1 in admin1_map:
                    admin1 = admin1_map[cc_admin1]
                if cc_admin2 in admin2_map:
                    admin2 = admin2_map[cc_admin2]

                write_row = {'lat':lat,'lon':lon,'name':name,'admin1':admin1,'admin2':admin2,'cc':cc}
                rows.append(write_row)
            writer.writeheader()
            writer.writerows(rows)

            if self.verbose:
                print('Removing extracted cities1000 to save space...')
            os.remove(cities1000_filename)

        # Load all the coordinates and locations
        geo_coords,locations = [],[]
        for row in rows:
            geo_coords.append((row['lat'],row['lon']))
            locations.append(row)
        ecef_coords = geodetic_in_ecef(geo_coords)
        return geo_coords,locations

def geodetic_in_ecef(geo_coords):
    geo_coords = np.asarray(geo_coords).astype(np.float)
    lat = geo_coords[:,0]
    lon = geo_coords[:,1]

    lat_r = np.radians(lat)
    lon_r = np.radians(lon)
    normal = A / (np.sqrt(1 - E2*(np.sin(lat_r) ** 2)))

    x = normal * np.cos(lat_r) * np.cos(lon_r)
    y = normal * np.cos(lat_r) * np.sin(lon_r)
    z = normal * (1 - E2) * np.sin(lat)

    return np.column_stack([x,y,z])

def rel_path(filename):
    return os.path.join(os.getcwd(), os.path.dirname(__file__), filename)

def get(geo_coord,mode=2,verbose=True):
    if type(geo_coord) != tuple or type(geo_coord[0]) != float:
        raise TypeError('Expecting a tuple')

    rg = RGeocoder(mode=mode,verbose=verbose)
    return rg.query([geo_coord])[0]

def search(geo_coords,mode=2,verbose=True):
    if type(geo_coords) != tuple and type(geo_coords) != list:
        raise TypeError('Expecting a tuple or a tuple/list of tuples')
    elif type(geo_coords[0]) != tuple:
        geo_coords = [geo_coords]
    
    rg = RGeocoder(mode=mode,verbose=verbose)
    return rg.query(geo_coords)

if __name__ == '__main__':
    print('Testing single coordinate through get...')
    city = (37.78674,-122.39222)
    print('Reverse geocoding 1 city...')
    result = get(city)
    print(result)

    print('Testing coordinates...')
    cities = [(51.5214588,-0.1729636),(9.936033, 76.259952),(37.38605,-122.08385)]
    print('Reverse geocoding %d cities...' % len(cities))
    results = search(cities)
    print(results)