import requests
import config
import json

from datetime       import datetime, timedelta
from urllib.request import urlopen
from urllib.parse   import urlencode

# 영화목록 받아오기
class Boxoffice(object):
    def __init__(self, movie_list_key):
        self.movie_list_key = movie_list_key

    def get_movies(self):
        targetDt = datetime.now() - timedelta(days=1)
        targetDt_str = targetDt.strftime('%Y%m%d')
        query_url = f"{config.KOFIC_DAILY_URL}?key={config.KOFIC_API_KEY}&targetDt={targetDt_str}"        
        print(query_url)
        with urlopen(query_url) as fin:
            return json.loads(fin.read().decode('utf-8'))

    def simplify(self, result):
        #print(result.get('boxOfficeResult').get('dailyBoxOfficeList'))
        return [
           {
              'rank': entry.get('rank'),
              'name': entry.get('movieNm'),
              'code': entry.get('movieCd')
           }
           for entry in result.get('boxOfficeResult').get('dailyBoxOfficeList')
        ]
    
box = Boxoffice(config.KOFIC_API_KEY)
movies = box.get_movies()
print(box.simplify(movies))


