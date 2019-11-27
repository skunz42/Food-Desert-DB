import googlemaps
import json
import urllib
import sys
import csv
from pymongo import MongoClient

'''***********************************************
                    findPlace
    purpose:
        gets json data from google search
    params:
        lat - represents latitude
        lng - represents longitude
        radius - represents search radius
        kw - represents search word (ie grocery)
        key - API authentication key
    return:
        jSonData - returns search in json format
***********************************************'''
def findPlace(lat, lng, radius, kw, key):
    #making the url
    AUTH_KEY = key #authentication key
    LOCATION = str(lat) + "," + str(lng) #location for url
    RADIUS = radius
    KEYWORD = kw #search word
    MyUrl = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json'
           '?location=%s'
           '&radius=%s'
           '&keyword=%s'
           '&sensor=false&key=%s') % (LOCATION, RADIUS, KEYWORD, AUTH_KEY) #url for search term
    #grabbing the JSON result
    response = urllib.request.urlopen(MyUrl)
    jsonRaw = response.read()
    jsonData = json.loads(jsonRaw)
    return jsonData

'''***********************************************
                    IterJson
    purpose:
        returns array of data parsed from search
        request
    params:
        place - jSonData retreived from search
    return:
        array of parsed data
***********************************************'''
def IterJson(place):
    x = {
        "Name": place['name'],
        "ID": place['reference'],
        "Latitude": place['geometry']['location']['lat'],
        "Longitude": place['geometry']['location']['lng'],
        "Address": place['vicinity'],
        "Rating": place['rating'],
        "Num Ratings": place['user_ratings_total']
    }
    return x

'''***********************************************
                    calcCoords
    purpose:
        calculates the coordinates to use when
        searching. Updates an array of tuples
        storing coordinates
    params:
        key - API authentication key
        coords - array of coordinates
        city - city being searched
    return:
        None
***********************************************'''
def calcCoords(key, coords, city):
    gmaps = googlemaps.Client(key=key) #authentication
    geocode_result = gmaps.geocode(city) #gets results for city
    nelat = geocode_result[0]['geometry']['bounds']['northeast']['lat'] #northeast latitude
    nelng = geocode_result[0]['geometry']['bounds']['northeast']['lng'] #northeast longitude
    swlat = geocode_result[0]['geometry']['bounds']['southwest']['lat'] #southwest latitude
    swlng = geocode_result[0]['geometry']['bounds']['southwest']['lng'] #southwest longitude
    km = 0.015

    templat = swlat #latitude and longitude used for calculation purposes
    templng = swlng

    while (templat <= nelat): #north/south calc
        while (templng <= nelng): #east/west calc
            coords.append((templat, templng))
            templng += km # ~ 1 km
        templng = swlng
        templat += km # ~ 1 km

'''***********************************************
                    writeCSV
    purpose:
        write data to csv
    params:
        places - list of grocery store dictionaries
        fn - filename
        city - city name
    return:
        None
***********************************************'''
def writeCSV(places, fn, city):
    minRatings = 30
    with open(fn, mode = 'w', newline = '') as csv_test:
        csv_writer = csv.writer(csv_test, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for p in places: # parse extraneous stores and spam entries and dollar stores
            if city in p['Address'] and int(p['Num Ratings']) > minRatings and "Dollar" not in p['Name']:
                csv_writer.writerow([p['ID'], p['Name'], p['Latitude'], p['Longitude'], p['Address'], p['Rating'], p['Num Ratings']])

'''***********************************************
                    writeDB
    purpose:
        write data to DB
    params:
        places - dict of grocery stores
        citystate - name of city that is being analyzed
    return:
        None
***********************************************'''
def writeDB(places, citystate):
    client = MongoClient(port=27017)
    db = client.CS432FP

    city = citystate[:len(citystate)-4] # gets city name
    state = citystate[len(citystate)-2:] #gets state abbreviation

    minRatings = 30

    for p in places:
        if city in p['Address'] and int(p['Num Ratings']) > minRatings and "Dollar" not in p['Name']:
            store = {
                'ID': p['ID'],
                'Name' : p['Name'],
                'City' : city,
                'State' : state,
                'Latitude': p['Latitude'],
                'Longitude' : p['Longitude'],
                'Address' : p['Address'],
                'Rating' : p['Rating'],
                'Num_Ratings' : p['Num Ratings'],
                'File Location' : "../" + city + "" + state
            }
            db.storeinfo.update({'_id':p['ID']}, store, upsert=True)

    print("Inserted documents")
    print(db.storeinfo.count())

'''***********************************************
                    scrapeData
    purpose:
        creates set of data
    parameters:
        fn - filename
        citystate - city + state for scraping
        city - city name for csv writing
    return:
        None
***********************************************'''
def scrapeData(fn, citystate, city):
    credsfile = open("../../Geo-Credentials/creds.txt", "r")
    keyval = credsfile.read()
    coords = []
    calcCoords(keyval, coords, citystate)

    gplaces = []
    for c in coords:
        gsearch = findPlace(c[0], c[1], 1000, 'grocery', keyval)
        if gsearch['status'] == 'OK':
            for place in gsearch['results']:
                storeInfo = IterJson(place)
                gplaces.append(storeInfo)

    #writeCSV(list({v['ID']:v for v in gplaces}.values()), fn, city) # insert unique elements into dictionary and make it a list
    # include call to writeDB
    writeDB(list({v['ID']:v for v in gplaces}.values()), citystate)

'''***********************************************
                    Main
***********************************************'''
def main():
    numArgs = 4
    if (len(sys.argv) != numArgs):
        print("Please input in the following format: python fetchstores.py <file> <city> <state abbrev>")
        return 1

    fn = "../DataFiles/" + str(sys.argv[1]) + ".csv"
    city = str(sys.argv[2])
    state = str(sys.argv[3])
    citystate = city + ", " + state

    scrapeData(fn, citystate, city)
main()
