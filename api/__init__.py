from flask      import Flask
from flask.globals import current_app, request
from flask_cors import CORS

from api.view                       import create_endpoints
from api.model.user_dao             import UserDao
from api.model.message_dao          import MessageDao
from api.model.theater_dao          import TheaterDao
from api.service.facebook_service   import FacebookMessage
from api.service.user_service       import UserService
from api.service.theater_service    import CGVTime

from config     import DB_CONNECTION_URL

class Service:
    pass

def create_app(database, facebook_credentials,google_credential):
    app = Flask(__name__)

    
    CORS(app)

    ##Persistence Layer -> model
    user_dao = UserDao(database)
    message_dao = MessageDao(database, user_dao)
    theater_dao = TheaterDao(database)
    
    ## Business Layer -> service
    services = Service()
    services.user_service = UserService(user_dao) 
    services.facebook_service = FacebookMessage(message_dao, theater_dao)
    services.theater_service  = CGVTime(theater_dao)

    ## Endpoint -> view
    create_endpoints(app, services, facebook_credentials, google_credential)

    return app
