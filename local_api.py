import config
from api import create_app

from sqlalchemy    import create_engine
from pymessenger   import Bot

database = create_engine(f"{config.DB_CONNECTION_URL}?charset=utf8")

facebook_credentials = {
    "FB_API_URL"                 : config.FB_API_URL,
    "VERIFY_TOKEN"               : config.VERIFY_TOKEN,
    "FACEBOOK_PAGE_ACCESS_TOKEN" : config.FACEBOOK_PAGE_ACCESS_TOKEN
}

movie_list_key = {
    "KOFIC_API_URL" : config.KOFIC_DAILY_URL,
    "KOFIC_API_KEY" : config.KOFIC_API_KEY
}

google_credential={
    "GOOGLE_API_KEY" : config.GOOGLE_API_KEY
}

app = create_app(database, facebook_credentials, google_credential)
