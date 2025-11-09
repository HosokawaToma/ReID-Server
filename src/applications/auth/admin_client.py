from modules.auth.parse_bearer import ModuleAuthParseBearer
from modules.auth.verify.admin_client import ModuleAuthVerifyAdminClient
from modules.auth.generate_token.admin_client import ModuleAuthGenerateTokenAdminClient
from entities.jwt.admin_client import EntityJWTAdminClient
from entities.admin_client import EntityAdminClient
from entities.environment.admin_client import EntityEnvironmentAdminClient
from entities.environment.jwt import EntityEnvironmentJwt

class ApplicationAuthAdminClient:
    def __init__(
        self,
        environment_admin_client: EntityEnvironmentAdminClient,
        parser: ModuleAuthParseBearer,
        verifier: ModuleAuthVerifyAdminClient,
        generator: ModuleAuthGenerateTokenAdminClient,
    ):
        self.environment_admin_client = environment_admin_client
        self.parser = parser
        self.verifier = verifier
        self.generator = generator

    def login(self, id: str, password: str) -> EntityAdminClient:
        if id != self.environment_admin_client.id or password != self.environment_admin_client.password:
            raise Exception("Invalid id or password")
        return EntityAdminClient(id=id, password=password)

    def parse(self, authorization: str) -> str:
        return self.parser(authorization)

    def verify(self, token: str) -> EntityJWTAdminClient:
        return self.verifier(token)

    def generate(self, id: str) -> str:
        return self.generator(id)

    @classmethod
    def create(
        cls,
        environment_jwt: EntityEnvironmentJwt,
        environment_admin_client: EntityEnvironmentAdminClient,
    ) -> "ApplicationAuthAdminClient":
        return cls(
            environment_admin_client=environment_admin_client,
            parser=ModuleAuthParseBearer(),
            verifier=ModuleAuthVerifyAdminClient(
                secret_key=environment_jwt.secret_key,
                algorithm=environment_jwt.algorithm,
                expire_minutes=environment_jwt.expire_minutes,
            ),
            generator=ModuleAuthGenerateTokenAdminClient(
                secret_key=environment_jwt.secret_key,
                algorithm=environment_jwt.algorithm,
                expire_minutes=environment_jwt.expire_minutes,
            ),
        )
