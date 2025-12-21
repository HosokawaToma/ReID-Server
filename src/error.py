class Error(Exception):
    def __init__(self, exception_classes: "BaseException | Error | None" = None):
        super().__init__()
        if exception_classes is None:
            self.exception_classes = []
        elif isinstance(exception_classes, Error):
            self.exception_classes = exception_classes.to_list()
        elif isinstance(exception_classes, BaseException):
            self.exception_classes = [exception_classes.__class__]

    def to_list(self) -> list[type[BaseException]]:
        return self.exception_classes + [self.__class__]

    def __str__(self):
        return "->".join([exception_class.__name__ for exception_class in self.to_list()])
