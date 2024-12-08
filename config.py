import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")

    MTX_API_HOST = os.getenv("MTX_API_HOST", "localhost")
    MTX_API_HOST_PORT = os.getenv("MTX_API_HOST_PORT", "9997")
    MTX_API_URI = "http://" + MTX_API_HOST + ":" + MTX_API_HOST_PORT

    MTX_HLS_HOST = os.getenv("MTX_LIVE_HOST", "localhost")
    MTX_HLS_HOST_PORT = os.getenv("MTX_LIVE_HOST_PORT", "8888")
    MTX_HLS_URI = MTX_HLS_HOST + ":" + MTX_HLS_HOST_PORT

    STREAMS_REDIRECT = "https://" + MTX_HLS_HOST

    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = os.getenv("MONGO_PORT", "27017")
    MONGO_USER = os.getenv("MONGO_USER", "root")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "root")
