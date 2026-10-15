
from fastapi import APIRouter, Request, Response, Header
from schemas.cokkie_schema import CookiePayload

router = APIRouter(prefix="/cookies", tags=["Cookies"])

# 1. POST
@router.post("/setcokkies")
async def set_cookie(
    payload: CookiePayload,
    response: Response,
    client_name: str = Header(...)
):
    response.set_cookie(
        key="employee_id",
        value=str(payload.employee_id),
        httponly=True,
        max_age=3600,
        samesite="lax",
    )

    response.set_cookie(
        key="employee_name",
        value=payload.employee_name,
        httponly=True,
        max_age=3600,
        samesite="lax",
    )

    response.set_cookie(
        key="age",
        value=str(payload.age),
        httponly=True,
        max_age=3600,
        samesite="lax",
    )

    response.headers["X-Client-Name"] = client_name

    return {"message": "Employee cookies set successfully"}


# 2. GET
@router.get("/read")
async def read_cookie(
    request: Request,
    client_name: str | None = Header(default=None)
):
    return {
        "employee_id": request.cookies.get("employee_id"),
        "employee_name": request.cookies.get("employee_name"),
        "age": request.cookies.get("age"),
        "client_name_header": client_name,
        "all_request_headers": dict(request.headers),
    }


# 3. DELETE
@router.delete("/delete")
async def delete_cookie(response: Response):
    response.delete_cookie("employee_id", path="/")
    response.delete_cookie("employee_name", path="/")
    response.delete_cookie("age", path="/")

    response.headers["X-Operation"] = "Cookie deletion"

    return {"message": "Employee cookies deleted successfully"}
