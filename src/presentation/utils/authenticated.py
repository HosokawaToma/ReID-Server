"""
プレゼンテーション用認証

Bearer トークンによる管理クライアント認証と、認証済み時の Depends 型を提供する。
"""
from typing import Annotated
from fastapi import Depends
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
    """
    OAuth2 認証アプリケーションを取得する。Depends 用。

    :param Environment environment: 環境設定
    :return ApplicationAdminClientAuthOAuth2: OAuth2 アプリケーション
    """
    return ApplicationAdminClientAuthOAuth2.create(environment)


def admin_client_authenticated(
    token: PresentationUtilTypeAuthorization,
    application: ApplicationAdminClientAuthOAuth2 = Depends(
        get_admin_client_auth_application),
) -> DtoAdminClientId:
    """
    Bearer トークンを検証し、認証済みの管理クライアントIDを返す。Depends 用。

    :param PresentationUtilTypeAuthorization token: Bearer トークン
    :param ApplicationAdminClientAuthOAuth2 application: OAuth2 アプリケーション
    :return DtoAdminClientId: 認証済み管理クライアントID
    :raises HTTPException: 認証失敗時（401）
    """
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
