import re
import requests
import json
import config

from flask            import request
from .movie_service   import Boxoffice
from .place_service   import FindCgvTheater
from .theater_service import CGVTime

class FacebookMessage:
    def __init__(self, message_dao, theater_dao):
        self.message_dao = message_dao
        self.theater_dao = theater_dao
    
    def get_current_state(self, sender_id):
        message = self.message_dao.get_state(sender_id)
        print('message5', message)
        if not message:
            return 'START'
        
        return message.next_state

    def get_previous_state(self, sender_id):
        message = self.message_dao.get_state(sender_id)
        
        return message.current_state

    def next_state(self, sender_id, message, current_state):
        if current_state == 'START':
            return 'RANK_OR_THEATER'
        elif current_state == 'RANK_OR_THEATER' and '순위' in message:
            next_state = 'RANK'
            return next_state
        elif current_state == 'RANK_OR_THEATER' and '영화관' in message:
            return 'THEATER'
        elif current_state == 'RANK_OR_THEATER' and 'Theater' in message:
            return 
        elif current_state == 'RANK' and '영화관' in message:
            return 'THEATER'
        elif current_state == 'THEATER' and 'Theater' in message:
            return 'SELECT'
        elif current_state == 'SELECT' and self.theater_dao.get_cgv_list(message):
            return 'TIME'
        elif current_state == 'THEATER' and '순위' in message:
            return 'RANK'
        elif current_state == 'TIME' and '영화관' in message:
            return 'SELECT'
        elif current_state == 'TIME' and '예매' in message:
            return 'CGV'
        elif current_state == 'TIME' and '나가기' in message:
            return 'LEAVE'
        elif current_state == 'CGV' and '다시' in message:
            return 'SELECT'
        elif current_state == 'CGV' and '나가기' in message:
            return 'LEAVE'
        elif current_state == 'LEAVE':
            return 'START'
        elif current_state == None:
            return 'START'
        elif current_state == 'BAD REQUEST' and '영화관' in message:
            return 'SELECT'
        elif current_state == 'BAD REQUEST' and '순위' in message:
            return 'RANK'
        else:
            return 'BAD REQUEST'
    
    def handling_bad_request(self, sender_id, next_state, message):
        if next_state == 'BAD REQUEST':
            state = self.get_previous_state(sender_id)
            next_state = self.next_state(sender_id, message, state)
            if state == '영화관':
                return 'SELECT'
            elif state == '순위':
                return 'RANK'
            else:
                return 'LEAVE'
    
    def save_message(self, sender_id, message, current_state, next_state):
        return self.message_dao.create_message(sender_id, message, current_state, next_state)

    def get_ranck_or_teater_message(self, sender_id, current_state, next_state):
        context = { 
                "text" : '반가워요!,\n\n원하는 영화를 알려드리고\n 가까운 영화관, 상영시간까지 알려드립니다.\n\n 영화순위 혹은 영화관 찾기를 입력해 보세요.',
                "quick_replies" : [
                    {
                    "content_type" : "text",
                    "title"        : "영화순위",
                    "payload"      : "<POSTBACK_PAYLOAD>"
                    },{
                    "content_type" : "text",
                    'title'        : "영화관 찾기",
                    "payload"      : "<POSTBACK_PAYLOAD>"
                    }
                ]
            }
        return {'context' : context}

    def get_rank_message(self, sender_id, current_state, next_state, message):
        box = Boxoffice(config.KOFIC_API_KEY)
        movies = box.get_movies()
        ranks = box.simplify(movies)
        #print(movies)
        #print(ranks)
        message_rank = ''.join(['{}. {} \n'.format(rank['rank'],rank['name']) for rank in ranks])
        context = {
                "text" : "요즘 볼만한 영화들의 순위입니다. \n\n{} \n 주변 CGV를 알아보고 싶으면 '영화관'을 입력해 주세요".format(message_rank),
                "quick_replies" :[
                    {
                    "content_type" : "text",
                    "title" : "영화관 찾기",
                    "payload" : "<POSTBACK_PAYLOAD>"
                        }
                ]}
        
        return {'context' : context}

    def get_theater_message(self, sender_id, current_state, next_state, message):
        location = FindCgvTheater(config.GOOGLE_API_KEY)
        cgvs = location.get_location()
        cgv_list = location.simplify(cgvs)
        if cgv_list:
            cgv_message = ''.join(['{}\n'.format(cgv['name'] ) for cgv in cgv_list])
            context = {
                    'text':'지금 주변에 있는 CGV 영화관 목록입니다. \n\n{} 입니다.\
                \n\n 영화 TOP10을 보고 싶으면  "영화순위"  를 CGV 영화시간표를 보고싶으면 원하시는 영화관 이름을 적어주시면 됩니다.'.format(cgv_message),
                    'quick_replies':[{
                        'content_type' : 'text',
                        'title' : '영화순위',
                        'payload' : '<POSTBACK_PAYLOAD>'
                        },{
                        'content_type' : 'text',
                        'title' : 'Theater',
                        'payload' : '<POSTBACK_PAYLOAD>'
                            }
                        ]
                    }
                
            return {'context': context}
        response = '현재 주변에는 CGV가 없습니다.'
        return {'response' : response}

    def get_select_message(self, sender_id, state, next_state, message):
        location = FindCgvTheater(config.GOOGLE_API_KEY)
        cgvs = location.get_location()
        cgv_list = location.simplify(cgvs)
        print('cgvs_list', cgv_list)

        context ={
                'text' : 'CGV를 골라주세요',
                'quick_replies' : [
                    {
                    'content_type' : 'text',
                    'title'        : cgv['name'],
                    'payload' : '<POSTBACK_PAYLOAD>'}for cgv in cgv_list[:13]]
                    }
        return {'context': context}
        

    def get_time_message(self, sender_id, current_state, next_state, message):
        try:
            cgv = CGVTime(self.theater_dao)
            today_movies = cgv.get_movies(message)
            today_movie_time = cgv.get_timtable(today_movies)
            print('today_movie_time',today_movie_time)
            movie_time = ','.join(['{}{}\n'.format(time[0], time[1:])for time in today_movie_time])
            print('=============', movie_time)

            context = {
                'text' : f'오늘 {message}의 영화시간은\n\n{movie_time}\n입니다.\n 영화관 선택으로 돌아가고 싶으면 "영화관" 을 입력해 주세요',
                'quick_replies' : [
                    {
                    'content_type' : 'text',
                        'title' : '영화관 돌아가기',
                        'payload' : '<POSTBACK_PAYLOAD>'
                        },{
                            'content_type' : 'text',
                            'title' : '예매하기',
                            'payload' : '<POSTBACK_PAYLOAD>'
                            }
                        ]}
        
            return {'context' : context}
        except:
            context = { 
                        "text" : '오늘 상영은 모두 종료되었습니다. ㅠㅠ\n 영화관 선택으로 돌아가고 싶으면 "영화관" 을 입력해 주세요',
                        'quick_replies' :[
                            {
                            'content_type' : 'text',
                            'title'        : '영화관 찾기',
                            'payload'      : '<POSTBACK_PAYLOAD>'
                            }
                        ]}
            return {'context' : context}
    
    def get_cgv_message(self, sender_id, state, next_state, message):
        cgv = CGVTime(self.theater_dao)
        print('========================3')
        cgv_code = cgv.get_cgv_code(message)
        print('cgv_code',cgv_code)
        url = f'http://www.cgv.co.kr/ticket/?MOVIE_CD=20025793&MOVIE_CD_GROUP=20025793&PLAY_YMD=20210405&THEATER_CD={cgv_code}'
        print('urls', url)
        buttons = [
                {
                'type' : 'web_url',
                'url' : f'http://www.cgv.co.kr/ticket/?MOVIE_CD=20025793&MOVIE_CD_GROUP=20025793&PLAY_YMD=20210405&THEATER_CD={cgv_code}',
                    'title' : '예매를 위해 CGV로 이동하기!'}]
        return {'title' : '예매를 위해 CGV로 이동하기', 'buttons' : buttons}

    def get_bad_request_message(self, sender_id, current_state, next_state, message):
        response = '잘못된 요청사항입니다. 다시 말씀해 주세요'
            
        return {'response' : response}

    def process_message(self, sender_id, current_state, next_state, message):
        print('ready2', sender_id, current_state,next_state)
        if next_state == 'RANK_OR_THEATER':
            return self.get_ranck_or_teater_message(sender_id, current_state, next_state)
        elif next_state == 'RANK':
            return self.get_rank_message(sender_id, current_state, next_state, message)
        elif next_state == 'THEATER':
            return self.get_theater_message(sender_id, current_state,next_state, message)
        elif next_state == 'SELECT':
            return self.get_select_message(sender_id,current_state, next_state, message)
        elif next_state == 'TIME':
            return self.get_time_message(sender_id, current_state, next_state, message)
        elif next_state == 'CGV':
            return self.get_cgv_message(sender_id, current_state, next_state, message)
        elif next_state == 'BAD REQUEST':
            return self.get_bad_request_message(sender_id, current_state, next_state, message)
