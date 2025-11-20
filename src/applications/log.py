class ApplicationLog:
    def __init__(self):
        pass

    def info(self, message: str):
        print(f"INFO: {message}")

    def warning(self, message: str):
        print(f"WARNING: {message}")

    def error(self, message: str):
        print(f"ERROR: {message}")

    def critical(self, message: str):
        print(f"CRITICAL: {message}")
