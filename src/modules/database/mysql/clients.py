from database.mysql import DatabaseMySQL
from database.mysql.models import DatabaseMySQLModelClient
from entities.client import EntityClient

class ModuleDatabaseMySQLClients:
    def __init__(self, database: DatabaseMySQL):
        self.database = database

    def create_client(self, client: EntityClient) -> None:
        with self.database as db_session:
            db_session.add(client.to_database_model())

    def get_client_by_id(self, client_id: str) -> EntityClient:
        with self.database as db_session:
            client_model = db_session \
                .query(DatabaseMySQLModelClient) \
                .filter(DatabaseMySQLModelClient.id == client_id) \
                .first()
            if client_model is None:
                raise Exception("Client not found in database")
            return EntityClient(
                id=client_model.id,
                hashed_password=client_model.hashed_password,
            )

    def update_client_by_id(self, client: EntityClient) -> None:
        with self.database as db_session:
            db_session \
            .query(DatabaseMySQLModelClient) \
            .filter(DatabaseMySQLModelClient.id == client.id) \
            .update({DatabaseMySQLModelClient.hashed_password: client.hashed_password})
