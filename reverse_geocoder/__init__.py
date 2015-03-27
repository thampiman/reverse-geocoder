##
# Author: Ajay Thampi
##
import os
import sys
import csv
csv.field_size_limit(sys.maxint)
import urllib
import zipfile
import collections
from scipy.spatial import cKDTree as KDTree
import time
import cKDTree_MP as KDTree_MP
import multiprocessing as mp

GN_URL = 'http://download.geonames.org/export/dump/'
GN_CITIES1000 = 'cities1000'
GN_ADMIN1 = 'admin1CodesASCII.txt'
GN_ADMIN2 = 'admin2Codes.txt'

# Columns from GN_URL
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

def singleton(cls):
    instances = {}
    def getinstance(mode=2):
        if cls not in instances:
            instances[cls] = cls(mode=mode)
        return instances[cls]
    return getinstance

@singleton
class RGeocoder:
    def __init__(self,mode=2):
        coordinates, self.locations = self.extract(rel_path(RG_FILE))
        self.mode = mode
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
            print 'Unable to parse coordinates:', coordinates
            raise e
        else:
            results = [self.locations[index] for index in indices]
            return results

    def extract(self,local_filename):
        if os.path.exists(local_filename):
            print 'Loading formatted geocoded file...'
            rows = csv.DictReader(open(local_filename,'rb'))
        else:
            gn_cities1000_url = GN_URL + GN_CITIES1000 + '.zip'
            gn_admin1_url = GN_URL + GN_ADMIN1
            gn_admin2_url = GN_URL + GN_ADMIN2

            cities1000_zipfilename = GN_CITIES1000 + '.zip'
            cities1000_filename = GN_CITIES1000 + '.txt'

            if not os.path.exists(cities1000_zipfilename):
                print 'Downloading files from Geoname...'
                urllib.urlretrieve(gn_cities1000_url,cities1000_zipfilename)
                urllib.urlretrieve(gn_admin1_url,GN_ADMIN1)
                urllib.urlretrieve(gn_admin2_url,GN_ADMIN2)

            print 'Extracting cities1000...'
            z = zipfile.ZipFile(open(cities1000_zipfilename,'rb'))
            open(cities1000_filename,'wb').write(z.read(cities1000_filename))

            print 'Loading admin1 codes...'
            admin1_map = {}
            t_rows = csv.reader(open(GN_ADMIN1,'rb'),delimiter='\t')
            for row in t_rows:
                admin1_map[row[ADMIN_COLUMNS['concatCodes']]] = row[ADMIN_COLUMNS['asciiName']]

            print 'Loading admin2 codes...'
            admin2_map = {}
            for row in csv.reader(open(GN_ADMIN2,'rb'),delimiter='\t'):
                admin2_map[row[ADMIN_COLUMNS['concatCodes']]] = row[ADMIN_COLUMNS['asciiName']]

            print 'Creating formatted geocoded file...'
            writer = csv.DictWriter(open(local_filename,'wb'),fieldnames=RG_COLUMNS)
            rows = []
            for row in csv.reader(open(cities1000_filename,'rb'),delimiter='\t'):
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

            print 'Removing extracted cities1000 to save space...'
            os.remove(cities1000_filename)

        # Load all the coordinates and locations
        coordinates,locations = [],[]
        for row in rows:
            coordinates.append((row['lat'],row['lon']))
            locations.append(row)
        return coordinates,locations

def rel_path(filename):
    return os.path.join(os.getcwd(), os.path.dirname(__file__), filename)

def get(coordinate,mode=2):
    rg = RGeocoder(mode=mode)
    return rg.query([coordinate])[0]

def search(coordinates,mode=2):
    rg = RGeocoder(mode=mode)
    return rg.query(coordinates)

if __name__ == '__main__':
    print 'Testing coordinates...'
    cities = [(-37.81, 144.96),(31.76, 35.21)]
    
    print 'Reverse geocoding %d cities...' % len(cities)
    results = search(cities)