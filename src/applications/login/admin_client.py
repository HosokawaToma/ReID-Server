from src.modules.database.mysql.clients import ModuleDatabaseMySQLClients
from src.modules.authenticator.admin_client import ModuleAuthenticatorAdminClient
from src.entities.environment.jwt import EntityEnvironmentJwt
from src.entities.environment.mysql import EntityEnvironmentMysql
from src.entities.admin_client import EntityAdminClient
from src.entities.environment.admin_client import EntityEnvironmentAdminClient

class ApplicationLoginAdminClient:
    def __init__(self, authenticator: ModuleAuthenticatorAdminClient, admin_client: EntityAdminClient):
        self.authenticator = authenticator
        self.admin_client = admin_client

    @classmethod
    def create(
        cls,
        environment_jwt: EntityEnvironmentJwt,
        environment_admin_client: EntityEnvironmentAdminClient,
    ) -> "ApplicationLoginAdminClient":
        return cls(
            authenticator=ModuleAuthenticatorAdminClient(
                secret_key=environment_jwt.secret_key,
                algorithm=environment_jwt.algorithm,
                expire_days=environment_jwt.expire_days,
            ),
            admin_client=EntityAdminClient(
                id=environment_admin_client.id,
                password=environment_admin_client.password,
            ),
        )

    def login(self, admin_client_id: str, password: str) -> str:
        if self.admin_client.id != admin_client_id or self.admin_client.password != password:
            raise Exception("Invalid admin_client_id or password")
        return self.authenticator.generate_token(self.admin_client)
