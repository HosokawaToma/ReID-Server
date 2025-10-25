from pymilvus import connections
from database.collections import DatabaseCollections

class Database:
    def __init__(self, name: str, host: str, port: str):
        self.connections = connections.connect(name, host=host, port=port)
        self.collections = DatabaseCollections.create()
