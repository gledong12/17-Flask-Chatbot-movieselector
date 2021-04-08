import pytest
import config

from sqlalchemy import create_engine, Text
from api        import create_app

test_db = create_engine(config.TEST_DB_CONNECTION_URL, encoding='utf-8')


facebook_credentials = {
    "FB_API_URL"                 : config.FB_API_URL,
    "VERIFY_TOKEN"               : config.VERIFY_TOKEN,
    "FACEBOOK_PAGE_ACCESS_TOKEN" : config.FACEBOOK_PAGE_ACCESS_TOKEN
}


google_credential={
    "GOOGLE_API_KEY" : config.GOOGLE_API_KEY
}

@pytest.fixture
def api():
    app = create_app(test_db,facebook_credentials, google_credential)
    app.config['TEST'] = True
    api = app.test_client()

    return api

def test_ping(api):
    result = api.get('/ping')
    
    print(result.data)

    assert b'pong' in result.dat

