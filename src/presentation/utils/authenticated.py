from typing import Type, TypeVar, Generic, Annotated
from fastapi import Depends
from applications import ApplicationBase
from environment import Environment
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from dto.admin_client.id import DtoAdminClientId
from dto.admin_client.auth.token import DtoAdminClientAuthToken
from error import AuthenticationError
from applications.admin_client.auth.oauth2 import ApplicationAdminClientAuthOAuth2


PresentationUtilTypeAuthorization = Annotated[str, Depends(
    OAuth2PasswordBearer(tokenUrl="token"))]


def get_admin_client_auth_application(
    environment: Environment = Depends(Environment)
) -> ApplicationAdminClientAuthOAuth2:
    return ApplicationAdminClientAuthOAuth2.create(environment)


def admin_client_authenticated(
    token: PresentationUtilTypeAuthorization,
    application: ApplicationAdminClientAuthOAuth2 = Depends(
        get_admin_client_auth_application),
) -> DtoAdminClientId:
    try:
        result = application.oauth2(
            DtoAdminClientAuthToken(token=token))
    except AuthenticationError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result


PresentationUtilAdminClientAuthenticated = Annotated[
    DtoAdminClientId, Depends(admin_client_authenticated)]
