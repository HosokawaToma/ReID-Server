from applications.admin_client.auth.login.credential import ApplicationAdminClientAuthLoginCredential
from entities.admin_client.auth.login.credential import AdminClientAuthLoginCredentialEntity
from presentation.admin_client.auth.login.credential.request import PresentationAdminClientAuthLoginCredentialRequest
from presentation.base import PresentationBase
from fastapi import JSONResponse

class PresentationAdminClientAuthLoginCredential(PresentationBase):
    def __init__(
        self,
        application: ApplicationAdminClientAuthLoginCredential
        ) -> None:
        self.application = application

    def endpoint(self, request: PresentationAdminClientAuthLoginCredentialRequest):
        try:
            self.application.login(AdminClientAuthLoginCredentialEntity(
                id=request.id,
                password=request.password
            ))
        except Exception as e:
            raise e
