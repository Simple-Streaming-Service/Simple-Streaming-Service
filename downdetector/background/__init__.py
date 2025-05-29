from downdetector import scheduler
from downdetector.services.subscription import broadcast
from downdetector.services.graphql import make_query
from downdetector import config
import requests


mediamtx_running = True
flask_running = True
graphql_running = True


def ping_mediamtx():
    global mediamtx_running
    response = requests.get(config.MTX_API_URI + "/v3/paths/list", timeout=int(config.MTX_API_TIMEOUT))
    if response.status_code == 200:
        if not mediamtx_running:
            broadcast("MediaMTX", "Соединение с сервером MediaMTX восстановлено!")
            mediamtx_running = True
    else:
        if mediamtx_running:
            broadcast("MediaMTX", "Соединение с сервером MediaMTX потеряно!")
            mediamtx_running = False

def ping_flask():
    global flask_running
    response = requests.get("http://localhost:5000/api/v1/user/auth", timeout=int(config.FLASK_API_TIMEOUT))
    if response.status_code == 200:
        if not flask_running:
            broadcast("Flask", "Соединение с сервером Flask восстановлено!")
            flask_running = True
    else:
        if flask_running:
            broadcast("Flask", "Соединение с сервером Flask потеряно!")
            flask_running = False

def ping_graphql():
    global graphql_running
    try:
        make_query("""
        query User {
            user(username: "any") {
                username
            }
        }
        """, {}, "http://localhost:5001", {}, timeout=int(config.GRAPHQL_API_TIMEOUT))
        if not graphql_running:
            broadcast("GraphQL", "Соединение с сервером GraphQL восстановлено!")
            graphql_running = True
    except:
        if graphql_running:
            broadcast("GraphQL", "Соединение с сервером GraphQL потеряно!")
            graphql_running = False


scheduler.add_job(ping_mediamtx, 'interval', minutes=1)
scheduler.add_job(ping_flask, 'interval', minutes=1)
scheduler.add_job(ping_graphql, 'interval', minutes=1)