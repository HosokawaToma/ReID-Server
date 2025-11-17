from database import Database
from database.models.camera_client import DatabaseModelCameraClient
from entities.camera_client import EntityCameraClient
from errors.modules.database import ErrorModuleDatabase

class ModuleDatabaseCameraClients:
    def __init__(self, database: Database):
        self.database = database

    def insert(self, camera_client: EntityCameraClient) -> None:
        with self.database as db_session:
            try:
                db_session.add(camera_client.to_database_model())
            except Exception as e:
                raise ErrorModuleDatabase(f"Failed to insert camera client: {e}")

    def select_by_id(self, camera_client_id: str) -> EntityCameraClient:
        try:
            with self.database as db_session:
                client_model = db_session \
                    .query(DatabaseModelCameraClient) \
                    .filter(DatabaseModelCameraClient.id == camera_client_id) \
                    .first()
                if client_model is None:
                    raise ErrorModuleDatabase("Camera client not found in database")
                return EntityCameraClient(
                    id=str(client_model.id),
                    password=None,
                    hashed_password=str(client_model.hashed_password),
                    camera_id=int(str(client_model.camera_id)),
                    view_id=int(str(client_model.view_id)),
                )
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to select camera client: {e}")

    def update_by_id(self, camera_client: EntityCameraClient) -> None:
        try:
            with self.database as db_session:
                db_session.query(DatabaseModelCameraClient) \
                    .filter(DatabaseModelCameraClient.id == camera_client.id) \
                    .update({DatabaseModelCameraClient.hashed_password: camera_client.hashed_password})
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to update camera client: {e}")
