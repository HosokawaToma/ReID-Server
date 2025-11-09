class ModuleAuthParse:
    HEADER_TYPE_KEY_OF_AUTHORIZATION = "Bearer"
    def __call__(self, authorization: str) -> str:
        header_type, token = authorization.split(" ")
        if not header_type:
            raise Exception("Invalid authorization header type")
        if header_type != self.HEADER_TYPE_KEY_OF_AUTHORIZATION:
            raise Exception("Invalid authorization header type")
        if not token:
            raise Exception("Invalid authorization token")
        return token
