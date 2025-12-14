from modules.auth.parse_bearer import ModuleAuthParseBearer
from modules.auth.verify.admin_client import ModuleAuthVerifyAdminClient
from modules.auth.generate_token.admin_client import ModuleAuthGenerateTokenAdminClient
from entities.jwt.admin_client import EntityJWTAdminClient
from entities.admin_client import EntityAdminClient
from environment import Environment

class ApplicationAuthAdminClient:
    def __init__(
        self,
        environment: Environment,
        parser: ModuleAuthParseBearer,
        verifier: ModuleAuthVerifyAdminClient,
        generator: ModuleAuthGenerateTokenAdminClient,
    ):
        self.environment = environment
        self.parser = parser
        self.verifier = verifier
        self.generator = generator

    def login(self, id: str, password: str) -> EntityAdminClient:
        if id != self.environment.admin_client_id or password != self.environment.admin_client_password:
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
        environment: Environment,
    ) -> "ApplicationAuthAdminClient":
        return cls(
            environment=environment,
            parser=ModuleAuthParseBearer(),
            verifier=ModuleAuthVerifyAdminClient(
                secret_key=environment.jwt_secret_key,
                algorithm=environment.jwt_algorithm,
                expire_minutes=environment.jwt_expire_minutes,
            ),
            generator=ModuleAuthGenerateTokenAdminClient(
                secret_key=environment.jwt_secret_key,
                algorithm=environment.jwt_algorithm,
                expire_minutes=environment.jwt_expire_minutes,
            ),
        )
