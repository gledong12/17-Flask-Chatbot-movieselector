import logging

from flask       import request, Flask, jsonify, make_response
from flask.helpers import make_response
from pymessenger import Bot

from ..service  import user_service

def create_endpoints(app, services, facebook_credentials, google_credential):
    
    @app.route('/ping', methods=['GET'])
    def ping():
        return 'pong'

    bot = Bot(facebook_credentials['FACEBOOK_PAGE_ACCESS_TOKEN'])
    
    @app.route('/', methods=['GET'])
    def validate_facebook_message():
        if not request.args.get('hub.verify_token') == facebook_credentials['VERIFY_TOKEN']:
            raise Exception("INVALED_TOKEN")
        return request.args.get('hub.challenge')
        
    @app.route("/", methods=['POST'])
    def facebook_message():
        if request.method == 'POST':
            payload = request.json
            sender_id = payload['entry'][0]['messaging'][0]['sender']['id']
            message   = payload['entry'][0]['messaging'][0]['message']['text']

            services.user_service.get_or_create_sender_id(sender_id)
            
            current_state = services.facebook_service.get_current_state(sender_id)
            next_state    = services.facebook_service.next_state(sender_id, message, current_state)
            message_id = services.facebook_service.save_message(sender_id, message, current_state, next_state)
            
            process_message = services.facebook_service.process_message(sender_id, current_state, next_state, message)
            if process_message:
                if process_message.get('context'):
                    bot.send_message(sender_id, process_message['context'])
                
                elif process_message.get('response'):
                    bot.send_text_message(sender_id, process_message['response'])

                elif process_message.get('buttons'):
                    bot.send_button_message(sender_id, process_message['title'],process_message['buttons'])
            return make_response(jsonify(process_message),200)
        else:
            return make_response(jsonify(message='INVALED_API'), 503)
