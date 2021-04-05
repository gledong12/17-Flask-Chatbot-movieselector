import requests
import datetime

from bs4 import BeautifulSoup as bs4

#url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0056&date=20210405'

#data = requests.get(url)
#html = data.text
# 영화이름 html selector
#body > div > div.sect-showtimes > ul > li:nth-child(1) > div > div.info-movie > a > strong

# 영화시간

#soup = bs4(html, 'html.parser')

#movies = soup.select('body > div > div.sect-showtimes > ul > li')

# 그날 상영하는 영화 제목 

class CGVTime():
    def __init__(self, theater_dao):
        self.theater_dao = theater_dao
    
    def get_movies(self, message):
        print('message4', message)
        cgvs_code = self.theater_dao.get_cgv_code(message)
        print('cgvs_code', cgvs_code)
        now =datetime.datetime.now().strftime('%Y%m%d')
        print(now)
        url = f'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode={cgvs_code}&date=20210406'
        print(url)
        data = requests.get(url)
        html = data.text
        soup = bs4(html, 'html.parser')
        movies = soup.select('body > div > div.sect-showtimes > ul > li')

        return movies

    

    def get_timtable(self, movies):
        movie_time_list = []
        #movies = soup.select('body > div > div.sect-showtimes > ul > li')
        for movie in movies:
            #time_list = []
            title = movie.select_one('div > div.info-movie > a > strong').get_text().strip()
            movie_time_list.append(title)
            timetables = movie.select('div > div.type-hall > div.info-timetable > ul > li')
            movie_time=[]
            for timetable in timetables:
                print(timetable)
                time = timetable.select_one('a > em').get_text()
                seat = timetable.select_one('a>span').get_text()
                if '마감' in time and '잔여좌석' not in seat:
                    continue
                else:
                    print(time)
                    seat = time + ',  ' + str(seat)
                    print(seat)
                movie_time_list.append(seat)
        return movie_time_list

    def get_cgv_code(self, message):
        now = datetime.datetime.now().strftime('%Y%m%d')
        cgv_code = self.theater_dao.get_cgv_code(message)
        tuple = (now, cgv_code)
        return tuple


