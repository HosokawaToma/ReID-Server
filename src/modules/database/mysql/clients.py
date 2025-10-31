from database.mysql import DatabaseMySQL
from entities.client import EntityClient
from database.mysql.models.client import DatabaseMySQLModelClient

class ModuleDatabaseMySQLClients:
    def __init__(self, database: DatabaseMySQL):
        self.database = database

    def create_client(self, client: EntityClient) -> None:
        with self.database as db_session:
            db_session.add(DatabaseMySQLModelClient(
                id=client.id,
                hashed_password=client.hashed_password,
            ))

    def select_by_id(self, id: str) -> EntityClient:
        with self.database as db_session:
            db_client = db_session.query(DatabaseMySQLModelClient).filter(DatabaseMySQLModelClient.id == id).first()
            if db_client is None:
                raise Exception("Client not found")
            return EntityClient(db_client.id, db_client.hashed_password)
