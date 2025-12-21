class Error(Exception):
    def __init__(self, exception_classes: "Exception | Error | None" = None):
        if exception_classes is None:
            self.exception_classes = []
        elif isinstance(exception_classes, Error):
            self.exception_classes = [
                exception_classes.__class__] + exception_classes.exception_classes
        elif isinstance(exception_classes, Exception):
            self.exception_classes = [exception_classes.__class__]

    def __str__(self):
        return "->".join([exception_class.__class__.__qualname__ for exception_class in self.exception_classes])
