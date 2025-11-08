from database import Database
from database.models.camera_client import DatabaseModelCameraClient
from entities.camera_client import EntityCameraClient

class ModuleDatabaseCameraClients:
    def __init__(self, database: Database):
        self.database = database

    def insert(self, camera_client: EntityCameraClient) -> None:
        with self.database as db_session:
            db_session.add(camera_client.to_database_model())

    def select_by_id(self, camera_client_id: str) -> EntityCameraClient:
        with self.database as db_session:
            client_model = db_session \
                .query(DatabaseModelCameraClient) \
                .filter(DatabaseModelCameraClient.id == camera_client_id) \
                .first()
            if client_model is None:
                raise Exception("Client not found in database")
            return EntityCameraClient(
                id=str(client_model.id),
                password=None,
                hashed_password=str(client_model.hashed_password),
                camera_id=int(str(client_model.camera_id)),
                view_id=int(str(client_model.view_id)),
            )

    def update_by_id(self, camera_client: EntityCameraClient) -> None:
        with self.database as db_session:
            db_session \
            .query(DatabaseModelCameraClient) \
            .filter(DatabaseModelCameraClient.id == camera_client.id) \
            .update({DatabaseModelCameraClient.hashed_password: camera_client.hashed_password})
