from flask import request, json

from app.api import bp
from app.models.service import FrontendChatService
from app.services.user import get_current_user


@bp.get("/services")
def services():
    """
    Service list endpoint.
    It retrieves a list of services from the database and returns them in a JSON response.
    :return: JSON response with services
    """
    objects = FrontendChatService.objects()
    shift = request.args.get("offset", 0, type=int)
    size = request.args.get("size", len(objects), type=int)
    return {"ok": True, "services": [service.name for service in objects[shift:shift + size]]}


@bp.get("/services/get")
def services_get():
    """
    Get service by name or id.
    Note: This endpoint is not implemented yet.
    :return: JSON response with service
    """
    return {"ok": False, "msg": "Not implemented!"}


@bp.post("/services/create")
def upload_service():
    """
    Service creation endpoint.
    It checks if the user is authorized and retrieves the data from the request.
    :return: JSON response with service
    """
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}
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
    """
    Service deletion endpoint.
    It checks if the user is authorized and retrieves the service name from the request.
    :return:
    """
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}
    # services = FrontendChatService.objects(author=user, name=request.args["name"])
    # services.delete()
    return {"ok": False, "msg": "Not implemented!"}


@bp.patch("services/update/name")
def update_service_name():
    """
    Service name update endpoint.
    Note: This endpoint is not implemented yet.
    :return:
    """
    return {"ok": False, "msg": "Not implemented!"}


@bp.patch("services/update/description")
def update_service_description():
    """
    Service description update endpoint.
    Note: This endpoint is not implemented yet.
    :return:
    """
    return {"ok": False, "msg": "Not implemented!"}


@bp.patch("services/update/code/initializer")
def update_service_initializer_code():
    """
    Service initializer code update endpoint.
    Note: This endpoint is not implemented yet.
    :return:
    """
    return {"ok": False, "msg": "Not implemented!"}


@bp.patch("services/update/code/converter")
def update_service_converter_code():
    """
    Service converter code update endpoint.
    Note: This endpoint is not implemented yet.
    :return:
    """
    return {"ok": False, "msg": "Not implemented!"}


@bp.patch("services/subscribe")
def subscribe_service():
    """
    Service subscription endpoint.
    Note: This endpoint is not implemented yet.
    :return:
    """
    return {"ok": False, "msg": "Not implemented!"}


@bp.patch("services/unsubscribe")
def unsubscribe_service():
    """
    Service unsubscription endpoint.
    Note: This endpoint is not implemented yet.
    :return:
    """
    return {"ok": False, "msg": "Not implemented!"}
