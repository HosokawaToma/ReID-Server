from errors.modules.auth.parse_bearer import ErrorModulesAuthParseBearer

class ModuleAuthParseBearer:
    HEADER_TYPE_KEY_OF_AUTHORIZATION = "Bearer"
    def __call__(self, authorization: str) -> str:
        header_type, token = authorization.split(" ")
        if not header_type:
            raise ErrorModulesAuthParseBearer("Empty authorization header type")
        if header_type != self.HEADER_TYPE_KEY_OF_AUTHORIZATION:
            raise ErrorModulesAuthParseBearer("Authorization header type is not Bearer")
        if not token:
            raise ErrorModulesAuthParseBearer("Empty authorization token")
        return token
