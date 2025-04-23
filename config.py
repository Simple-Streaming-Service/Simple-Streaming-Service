import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")

    MTX_API_TIMEOUT = os.getenv("MTX_API_TIMEOUT", "1000")
    MTX_API_HOST = os.getenv("MTX_API_HOST", "localhost")
    MTX_API_HOST_PORT = os.getenv("MTX_API_HOST_PORT", "9997")
    MTX_API_URI = "http://" + MTX_API_HOST + ":" + MTX_API_HOST_PORT

    MTX_HLS_HOST = os.getenv("MTX_LIVE_HOST", "localhost")
    MTX_HLS_HOST_PORT = os.getenv("MTX_LIVE_HOST_PORT", "8888")
    MTX_HLS_URI = MTX_HLS_HOST + ":" + MTX_HLS_HOST_PORT

    STREAMS_REDIRECT = "https://" + MTX_HLS_URI

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "27017")
    DB_USERNAME = os.getenv("DB_USERNAME", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
    DB_NAME = os.getenv("DB_NAME", "video_service")
    MONGO_URI = f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin"
    NEO4J_URI = f"bolt://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
