import os
import requests
from requests.models import LocationParseError
import config
import json
import re

from flask          import Flask 
from dotenv         import load_dotenv
from urllib.request import urlopen

# geolocation_api - 경도, 위도 추출 후 주변 영화관 검색

load_dotenv(verbose=True)

class FindCgvTheater(object):
    def __init__(self, google_credentials):
        self.google_credentials = google_credentials

    def get_location(self):
        geolocation_url=f'https://www.googleapis.com/geolocation/v1/geolocate?key={config.GOOGLE_API_KEY}' 
        data = {
            'considerIp' : True
            }
        requestpost = requests.post(geolocation_url, json=data)
        respons_data = requestpost.json()
        lat = respons_data['location']['lat']
        lng = respons_data['location']['lng']

        Place_url ="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius=30000&type=movie_theater&keyword=CGV&key={}".format(lat,lng,config.GOOGLE_API_KEY)

        place_result = requests.post(Place_url)
        #place_data = place_result.json()
        #results = place_data['results']

        return place_result.json()
    
    def simplify(self, results):

        return [
            {
                'name' : result['name']
            } for result in results['results'] if re.match('CGV', result['name'])]

location = FindCgvTheater(config.GOOGLE_API_KEY)
get_cgv = location.get_location()
cgvs_list = list(get_cgv.keys())
#print(get_cgv)
#print(location.simplify(get_cgv))
