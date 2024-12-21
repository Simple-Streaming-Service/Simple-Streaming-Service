from app.api import bp


@bp.get("/services")
def services():
    return {"ok": False, "msg": "Not implemented!"}

@bp.post("/create/service")
def upload_service():
    return {"ok": False, "msg": "Not implemented!"}

@bp.post("/delete/service")
def delete_service():
    return {"ok": False, "msg": "Not implemented!"}

@bp.patch("/update/service/name")
def update_service_name():
    return {"ok": False, "msg": "Not implemented!"}

@bp.patch("/update/service/code")
def update_service_code():
    return {"ok": False, "msg": "Not implemented!"}