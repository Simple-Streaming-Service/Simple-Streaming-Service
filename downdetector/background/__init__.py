from downdetector import scheduler
from downdetector.services.subscription import broadcast
from downdetector.services.graphql import make_query
from downdetector import config
import requests


mediamtx_running = 1
flask_running = 1
graphql_running = 1


def ping_media_mtx() -> bool:
    global mediamtx_running
    try:
        requests.get(config.MTX_API_URI + "/v3/paths/list", timeout=int(config.MTX_API_TIMEOUT))
        if mediamtx_running <= 0:
            broadcast("MediaMTX", "❗[[MediaMTX]]: ✅ Соединение с сервером восстановлено!")
            mediamtx_running = 1
        return True
    except:
        if mediamtx_running == -10:
            broadcast("MediaMTX", "❗❗❗[[MediaMTX]]: ❌ Сервер не отвечает долгое время!")
        else:
            if mediamtx_running > 0:
                broadcast("MediaMTX", "❗[[MediaMTX]]: ❌ Соединение с сервером потеряно!")
        mediamtx_running -= 1
        return False

def ping_flask() -> bool:
    global flask_running
    try:
        requests.post("http://localhost:5000/api/v1/bot/auth", timeout=int(config.MTX_API_TIMEOUT))
        if flask_running <= 0:
            broadcast("Flask", "❗[[Flask]]: ✅ Соединение с сервером восстановлено!")
            flask_running = 1
        return True
    except:
        if flask_running == -10:
            broadcast("Flask", "❗❗❗[[Flask]]: ❌ Сервер не отвечает долгое время!")
        else:
            if flask_running > 0:
                broadcast("Flask", "❗[[Flask]]: ❌ Соединение с сервером потеряно!")
        flask_running -= 1
        return False

def ping_graphql() -> bool:
    global graphql_running
    try:
        make_query("""
        query User {
            user(username: "any") {
                username
            }
        }
        """, {}, "http://localhost:5001", {}, int(config.MTX_API_TIMEOUT))
        if graphql_running <= 0:
            broadcast("GraphQL", "❗[[GraphQL]]: ✅ Соединение с сервером восстановлено!")
            graphql_running = 1
        return True
    except:
        if graphql_running == -10:
            broadcast("GraphQL", "❗❗❗[[GraphQL]]: ❌ Сервер не отвечает долгое время!")
        else:
            if graphql_running > 0:
                broadcast("GraphQL", "❗[[GraphQL]]: ❌ Соединение с сервером потеряно!")
        graphql_running -= 1
        return False


scheduler.add_job(ping_media_mtx, 'interval', minutes=1)
scheduler.add_job(ping_flask, 'interval', minutes=1)
scheduler.add_job(ping_graphql, 'interval', minutes=1)