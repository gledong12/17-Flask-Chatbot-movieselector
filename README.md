# Donplayer
[![Dongplayer](https://images.velog.io/images/eagle5424/post/550801dd-4467-4669-8c7c-2c296bd69506/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7,%202021-06-14%2016-21-06.png)](https://www.youtube.com/watch?v=1uyhBPQEWqs)


## 2021.03.29 ~ 2021.04.06
Search for nearby movie theaters and send them the title and movie time.

## Project Structure
```
├── api
│   ├── model
│   │   ├── theater_dao.py
│   │   ├── user_dao.py
│   │   └── message_dao.py
│   ├── service
│   │   ├── __init__.py
│   │   ├── facebook_service.py
│   │   ├── message_service.py
│   │   ├── movie_service.py
│   │   ├── place_service.py
│   │   ├── theater_service.py
│   │   └── user_service.py
│   └── user_service.py
│      └── __init__.py
└── local_api.py
```
* `API`: Include API function code related to search the movie theater
    * `model` : This folder collects file that only have access to the database
        * `thater_dao` : This file is a collection of data related to movie theaters and related services
        * `user_dao` : This file is a collection of data related to user statement and related services
        * `message_dao` : This file is a collection of data related to messages and related services 
    * `Service` : Include the business code related to search movie theater
        * `facebook_service.py` : The collecction of service linked to Facebook Messenger
        * `message_service.py` : The collection of service send to message
        * `movie_service.py`   : The collection of get movie time and the remaining seat from movie hompage
        * `place_service.py` : The collection of search movie theater at the current location
        * `user_service.py` : The collection of handleing user statement
    * `view` : The function is that show full or subscription category userlist.
        * `__init__.py` : Create endpoint

## User statement
<div align="center">
  <img src="https://images.velog.io/images/eagle5424/post/ce4defff-22cf-4382-980e-29b2d2b56a7e/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7,%202021-04-13%2000-27-26.png"><br>
</div>

* `START`   : User get this statement when chatbot start
* `Rank or Theater` : User get next statement when chatbot start.
* `RANK`    : If the current status is 'rank or heater', the user enters '순위' and gets today's box office top 10.
* `THEATER` : If the current status is 'rank or heater', the user enters '영화관' and navigates the nearby movie theater.
Of course, the 'RANK' phase and 'THEATER' states can go back and forth from one another.
* `SELECT` : In the 'THEATER' step, select the movie theater you searched for and choose the CGV you want to know.
* `TIME`   : It is a stage that shows the title and time of the movie theater selected during the 'SELECT' stage.
* `CGV`    : Steps to link to a web page for reservation
* `BAD REQUEST` : In that situation, this stage can return to the 'RANK' and 'THEATER' stages as the state you get when you don't get the word you want.

## chatbot?
챗봇 혹은 채터봇은 음성이나 문자를 통한 인간과의 대화를 통해서 특별한 작업을 수행하도록 제작된 컴퓨터 프로그램이다.
In that situation, this stage can return to the 'RANK' and 'THEATER' stages as the state you get when you don't get the word you want.

## STACK
PYTHON / FLASK / MYSQL / GIT / GITHUB / FACEBOOK_Messenger_API / Geolocation_API / Place_API / SLACK / Beautifulsoup
---
# 구현목록
1. FLASK를 사용해 Layered Architecture의 디자인 패턴으로 개발
2. yoyo-migration을 사용해 데이터베이스 테이블 생성
3. FACEBOOK_Messenger_API를 사용해 Chatbot 구현
4. 영화진흥위원회_API를 사용해 BOXOFFICE TOP 10 채팅 구현
5. Geolocation_API, Place_API를 사용해 내 주변의 영화관 검색 기능 구현
6. Beautifulsoup을 사용해 CGV 웹페이지 크롤링을 통한 해당 영화관의 영화제목별 상영시간 안내 구현
7. PYTHON을 사용해 User의 상태관리 구현
