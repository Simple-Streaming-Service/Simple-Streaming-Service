import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    if len(SECRET_KEY) == 0: SECRET_KEY = "secret"

    MTX_API_HOST = os.getenv("MTX_API_HOST", "localhost")
    if len(MTX_API_HOST) == 0: MTX_API_HOST = "localhost"
    MTX_API_HOST_PORT = os.getenv("MTX_API_HOST_PORT", "9997")
    if len(MTX_API_HOST_PORT) == 0: MTX_API_HOST_PORT = "9997"
    MTX_API_URI = "http://" + MTX_API_HOST + ":" + MTX_API_HOST_PORT

    MTX_HLS_HOST = os.getenv("MTX_LIVE_HOST", "localhost")
    if len(MTX_HLS_HOST) == 0: MTX_HLS_HOST = "localhost"
    MTX_HLS_HOST_PORT = os.getenv("MTX_LIVE_HOST_PORT", "8888")
    if len(MTX_HLS_HOST_PORT) == 0: MTX_HLS_HOST_PORT = "8888"
    MTX_HLS_URI = MTX_HLS_HOST + ":" + MTX_HLS_HOST_PORT

    STREAMS_REDIRECT = "https://" + MTX_HLS_URI

    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    if len(MONGO_HOST) == 0: MONGO_HOST = "localhost"
    MONGO_PORT = os.getenv("MONGO_PORT", "27017")
    if len(MONGO_PORT) == 0: MONGO_PORT = "27017"
    MONGO_USER = os.getenv("MONGO_USER", "root")
    if len(MONGO_USER) == 0: MONGO_USER = "root"
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "root")
    if len(MONGO_PASSWORD) == 0: MONGO_PASSWORD = "root"
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "video_service")
    if len(MONGO_DB_NAME) == 0: MONGO_DB_NAME = "video_service"
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"
