from flask import request, json

from app.api import bp
from app.models.service import FrontendChatService
from app.services.user import get_current_user


@bp.get("/services")
def services():
    objects = FrontendChatService.objects()
    shift = request.args.get("offset", 0, type=int)
    size = request.args.get("size", len(objects), type=int)
    return {"ok": True, "services": [service.name for service in objects[shift:shift + size]]}

@bp.get("/services/get")
def services_get():
    return {"ok": False, "msg": "Not implemented!"}

@bp.post("/services/create")
def upload_service():
    user = get_current_user()
    if not user: return {"ok": False, "error": "User not authorized!"}
    data = dict(json.loads(request.data))
    try:
        service = FrontendChatService(
            name=data["name"],
            description=data["description"],
            author=user,
            initializer_code=data.get("initializer_code", ""),
            converter_code=data.get("converter_code", "")
        )
        service.validate()
        service.save()
    except Exception as e:
        return {"ok": False, "error": "Service creation error!", "exception": str(e)}
    return {"ok": True, "msg": "Service created successfully!"}

@bp.post("/services/delete")
def delete_service():
    user = get_current_user()
    if not user: return {"ok": False, "error": "User not authorized!"}
    # services = FrontendChatService.objects(author=user, name=request.args["name"])
    # services.delete()
    return {"ok": False, "msg": "Not implemented!"}

@bp.patch("services/update/name")
def update_service_name():
    return {"ok": False, "msg": "Not implemented!"}

@bp.patch("services/update/description")
def update_service_description():
    return {"ok": False, "msg": "Not implemented!"}

@bp.patch("services/update/code/initializer")
def update_service_initializer_code():
    return {"ok": False, "msg": "Not implemented!"}

@bp.patch("services/update/code/converter")
def update_service_converter_code():
    return {"ok": False, "msg": "Not implemented!"}

@bp.patch("services/subscribe")
def subscribe_service():
    return {"ok": False, "msg": "Not implemented!"}

@bp.patch("services/unsubscribe")
def unsubscribe_service():
    return {"ok": False, "msg": "Not implemented!"}