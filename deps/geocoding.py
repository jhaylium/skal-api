import requests
from configparser import ConfigParser
import json
import datetime as dt
from pprint import pprint as pp


class Location:

    def __init__(self):
        cfg = ConfigParser()
        cfg.read('skalcred.ini')
        self.googleApiKey = cfg.get('locations', 'googleApiKey')
        self.arcGisApiKey = cfg.get('locations', 'arcGisKey')
        self.runDate =  dt.datetime.now().strftime('%m.%d.%YT%H.%M.%S')


    def googleReverseGeocode(self, lat, lng):
        file = open("geocodingResults.txt", "a")
        file.write("Google Reverse Geocode started at " + self.runDate + "\n")

        print('Reverse Geocode Started')
        geocodeApiUrl = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}'#.format(lat, lng, apiKey )#lat,lng,apiKey

        r = requests.get(geocodeApiUrl.format(lat, lng, self.googleApiKey))
        data = r.json()
        print('Reverse Geocode Request Complete')
        file.write("Google API Status is " + data['status'] + "\n")
        if data['status'] == 'OK':
            response = data['results']
            baseResult = response[0]
            print(baseResult)
            address = baseResult['formatted_address']
            for i in baseResult['address_components']:
                # print(i)
                if i['types'][0] == 'administrative_area_level_1':
                    state = i['long_name']
                if i['types'][0] == 'country':
                    country = i['short_name']
                if i['types'][0] == 'locality':
                    city = i['long_name']
                if i['types'][0] == 'postal_code':
                    postalCode = i['long_name']

            file.write('Google API Reverse Geocode Ran Successfully \n')
            file.close()
            return {'address':address, 'province':state, 'country':country, 'city':city, 'postalCode':postalCode}
        else:
            file.write('Error Code: ' + data["error_message"] + "\n")
            file.write("Did not Connect with Google Services Wrote Google Failure. \n")
            file.close()
            return 'Google Failure'

    def arcGisReverseGeocode(self, lat, lng):
        print('***ArcGIS Call***')
        format = 'json'
        token = self.arcGisApiKey
        langCode = 'EN'
        baseUrl = 'http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode?location={},{}&f={}&featureTypes='
        url = baseUrl.format(lng, lat,format,langCode)
        r = requests.get(url)
        data = r.json()
        result = data['address']
        name = result['Match_addr']
        address = result['Address']
        longAddress = result['LongLabel']
        city = result['City']
        province = result['Region']
        country = result['CountryCode']
        postalCode = result['Postal']

        return {'name':name,'address': address, 'province': province, 'country': country, 'city': city, 'postalCode': postalCode,'longAddress':longAddress}


    def googlePlaceSearch(self, address):
        print('***Google Places Search')
        file = open('geocodingResults.txt', "a")
        file.write("Google Places Search has begun " + self.runDate + "\n")
        fields = 'formatted_address,icon,id,name,place_id,types'
        searchInput = address
        inputType = 'textquery'
        # bias =
        baseUrl = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype={}&fields={}&key={}'
        url = baseUrl.format(searchInput, inputType, fields, self.googleApiKey)
        r = requests.get(url)
        data = r.json()
        file.write("Google Places Status Code " + data['status'] + "\n")
        results = data['candidates'][0]
        address = results['formatted_address']
        # geometry = results['geometry']
        # icon = results['icon']
        id = results['id']
        name = results['name']
        # permanently_closed = results['permanently_closed']
        # photos = results['photos']
        place_id = results['place_id']
        # plus_code = results['plus_code']
        # scope = results['scope']
        types = results['types']
        file.write("Google Places Search has completed \n")
        file.close()
        return {'address':address,'id':id, 'name':name,'place_id':place_id,'type':types}


    def googlePlaceDetails(self, placeID):
        file = open("geocodingResults.txt", "a")
        file.write("Google Place Details has started " + self.runDate + "\n")
        print('***Google Place Details***')
        fields = 'address_component,adr_address,alt_id,formatted_address,geometry,icon,id,name,permanently_closed,photo,place_id,plus_code,scope,type,url,utc_offset,vicinity'
        # fields='name'
        baseUrl = r'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&fields={}&key={}'
        url = baseUrl.format(placeID, fields, self.googleApiKey)
        r = requests.get(url)
        data = r.json()
        file.write("Google Places Details Status Code: " + data['status'] + "\n")
        results = data['result']
        name = results['name']
        address = results['formatted_address']
        file.close()
        return {'name':name, 'address':address}



    def getLocation(self, lat, lng):

        arcCall = self.googleReverseGeocode(lat,lng)
        gFailed = 'Google Failure'
        if arcCall == "Google Failure":
            address = gFailed
            city = gFailed
            state = gFailed
            country = gFailed
            name = gFailed
        else:
            address = arcCall['address']
            city = arcCall['city']
            state = arcCall['province']
            country = arcCall['country']
            googleSearch = self.googlePlaceSearch(address)
            placeId = googleSearch['place_id']
            googleName = self.googlePlaceDetails(placeId)
            name = googleName['name']
        return [name, address, city, state, country]



