from flask import request, json

from app.api import bp
from app.models.account import User
from app.models.service import FrontendChatService
from app.services.user import get_current_user


@bp.get("/services")
def services():
    objects = FrontendChatService.nodes.all()
    shift = request.args.get("offset", 0, type=int)
    size = request.args.get("size", len(objects), type=int)
    return {"ok": True, "services": [service.name for service in objects[shift:shift + size]]}

@bp.get("/services/<name>")
def services_get(name : str):
    service = FrontendChatService.nodes.first_or_none(name=name)
    if service is None:
        return { "ok": False, "error": "Service not found!" }
    return {
        "ok": True,
        "service":{
            "name": service.name,
            "description": service.description,
            "author": service.author.single(),
            "initializer_code": service.initializer_code,
            "formatter_code": service.formatting_code
        }
    }

@bp.post("/services/<name>")
def upload_service(name : str):
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    data = dict(json.loads(request.data))
    try:
        service = FrontendChatService(
            name=name,
            description=data["description"],
            initializer_code=data.get("initializer_code", ""),
            formatting_code=data.get("formatting_code", "")
        )
        service.save()
        service.author.connect(user)
    except Exception as e:
        return {"ok": False, "error": "Service creation error!", "exception": str(e)}
    return {"ok": True, "msg": "Service created successfully!"}

@bp.delete("/services/<name>")
def delete_service(name : str):
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    service = FrontendChatService.nodes.first_or_none(name=name)
    if service is None:
        return { "ok": False, "error": "Service not found!" }
    if user not in service.author:
        return { "ok": False, "error": "You are not author of this service!" }
    service.delete()
    service.save()
    return {"ok": True, "msg": "Service deleted successfully!"}

@bp.patch("services/<name>/name")
def update_service_name(name : str):
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    service = FrontendChatService.nodes.first_or_none(name=name)
    if service is None:
        return {"ok": False, "error": "Service not found!"}
    if user not in service.author:
        return {"ok": False, "error": "You are not author of this service!"}
    data = dict(json.loads(request.data))
    service.name = data["name"]
    service.save()
    return {"ok": True, "msg": "Service name updated successfully!"}

@bp.patch("services/<name>/author")
def update_service_author(name : str):
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    service = FrontendChatService.nodes.first_or_none(name=name)
    if service is None:
        return {"ok": False, "error": "Service not found!"}
    if user not in service.author:
        return {"ok": False, "error": "You are not author of this service!"}
    data = dict(json.loads(request.data))
    new_author = User.nodes.first_or_none(name=data["author"])
    if not new_author: return {"ok": False, "error": "New author not found!"}
    service.author.disconnect(user)
    service.author.connect(new_author)
    return {"ok": True, "msg": "Service author updated successfully!"}

@bp.patch("services/<name>/description")
def update_service_description(name : str):
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    service = FrontendChatService.nodes.first_or_none(name=name)
    if service is None:
        return {"ok": False, "error": "Service not found!"}
    if user not in service.author:
        return {"ok": False, "error": "You are not author of this service!"}
    data = dict(json.loads(request.data))
    service.description = data["description"]
    service.save()
    return {"ok": True, "msg": "Service description updated successfully!"}

@bp.patch("services/<name>/code/initializer")
def update_service_initializer_code(name : str):
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    service = FrontendChatService.nodes.first_or_none(name=name)
    if service is None:
        return {"ok": False, "error": "Service not found!"}
    if user not in service.author:
        return {"ok": False, "error": "You are not author of this service!"}
    data = dict(json.loads(request.data))
    service.initializer_code = data["code"]
    service.save()
    return {"ok": True, "msg": "Service initializer code updated successfully!"}

@bp.patch("services/<name>/code/formatting")
def update_service_converter_code(name : str):
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    service = FrontendChatService.nodes.first_or_none(name=name)
    if service is None:
        return {"ok": False, "error": "Service not found!"}
    if user not in service.author:
        return {"ok": False, "error": "You are not author of this service!"}
    data = dict(json.loads(request.data))
    service.formatting_code = data["code"]
    service.save()
    return {"ok": True, "msg": "Service formatting code updated successfully!"}

@bp.post("services/<name>/subscribe")
def subscribe_service(name : str):
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    profile = user.profile.single()
    if not profile: return {"ok": False, "error": "User not streamer!"}
    service = FrontendChatService.nodes.first_or_none(name=name)
    if service is None:
        return {"ok": False, "error": "Service not found!"}
    profile.services.connect(service)
    return {"ok": True, "msg": "Subscribed to service!"}

@bp.post("services/<name>/unsubscribe")
def unsubscribe_service(name : str):
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    profile = user.profile.single()
    if not profile: return {"ok": False, "error": "User not streamer!"}
    service = FrontendChatService.nodes.first_or_none(name=name)
    if service is None:
        return {"ok": False, "error": "Service not found!"}
    profile.services.disconnect(service)
    return {"ok": True, "msg": "Unsubscribed from service!"}