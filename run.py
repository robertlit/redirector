from app.data import RedisDataStore
from app.redirector import create_app

if __name__ == "__main__":
    app = create_app(RedisDataStore(decode_responses=True))
    app.run()
