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
    
    def get_cgv_code(self, message):
        cgv = self.theater_dao.get_cgv_code

        for i in cgv:
            if message == i[1]:
                return i[2]

    
    def get_movies(self, message):
        print('message4', message)
        cgvs_code = self.get_cgv_code(message)[1]
        print('cgvs_code', cgvs_code)
        now =datetime.datetime.now().strftime('%Y%m%d')
        print(now)
        url = f'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode={cgvs_code}&date=20210412'
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
                time=[]
                time = timetable.select_one('a > em').get_text()
                print('time2', time)
                seat = timetable.select_one('a>span').get_text()
                print('seats', seat)
                if '마감' not in time and '잔여좌석' in seat:
                    time, seat
                else:
                    time.append(time)
                    time.append(seat)
                seat = time + ',  ' + str(seat)
                print(seat)
                movie_time_list.append(seat)
            print(movie_time_list)
        return movie_time_list

    def get_cgv_code(self, message):
        print('message7', message)
        now = datetime.datetime.now().strftime('%Y%m%d')
        cgvs = self.theater_dao.get_cgv_code(message)
        for cgv in cgvs:
            if message in cgv[1]:
                cgv = cgv[2]
                print('cgv_code', cgv)
                tuple = (now, cgv)
                return tuple


