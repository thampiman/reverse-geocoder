from timeit import timeit
import csv
import reverse_geocoder as rg

if __name__ == '__main__':
    setup = "import csv;import reverse_geocoder as rg;print('Loading coordinates...');" + \
            "cities = [(row[0],row[1]) for row in csv.reader(open('../test/coordinates_10000000.csv','rt'),delimiter='\t')];"
    num = 3
    t = timeit(stmt="rg.search(cities,mode=1)",setup=setup,number=num)
    print('Running time: %.2f secs' % (t / num))

    print('\nLoading coordinates to compare mode 1 and mode 2...')
    cities = [(row[0],row[1]) for row in csv.reader(open('../test/coordinates_1000.csv','rt'),delimiter='\t')]
    result1 = rg.search(cities,mode=1)
    result2 = rg.search(cities,mode=2)
    if result1 != result2:
        print('Results do not match!')
    else:
        print('Both results match!')