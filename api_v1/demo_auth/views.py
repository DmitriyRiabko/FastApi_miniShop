from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
import secrets


router = APIRouter(prefix="/demo_auth", tags=["demo_auth"])

security = HTTPBasic()


@router.get("/basic-auth")
def demo_basic_auth_credentionals(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "message": "Hi",
        "username": credentials.username,
        "password": credentials.password,
    }
    pass


username_to_passwords = {
    "admin": "admin",
    "john": "password",
}

static_auth_token_to_username = {
    "ghthfjkdold": "admin",
    "fgpkdjkdgjdkdfjg": "john",
}


def get_auth_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
        headers={"WWW-authenticate": "Basic"},
    )
    correct_password = username_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc

    if not secrets.compare_digest(
        credentials.password.encode("utf-8"), correct_password.encode("utf-8")
    ):
        raise unauthed_exc

    return credentials.username


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token"),
) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
    )


@router.get("/basic-auth-username")
def demo_basic_auth_username(auth_username: str = Depends(get_auth_username)):
    return {"message": f"Hi {auth_username}", "username": auth_username}


@router.get("/some-http-header-auth")
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token),
):
    return {"message": f"Hi {username}", "username": username}
