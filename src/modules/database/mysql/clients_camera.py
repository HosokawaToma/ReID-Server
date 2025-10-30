from database.mysql.models import DatabaseMySQLModelClientCamera
from entities.client_camera import EntityClientCamera
from database.mysql import DatabaseMySQL

class ModuleDatabaseMySQLClientsCamera:
    def __init__(self, database: DatabaseMySQL):
        self.database = database

    def create_client_camera_by_id(self, client_camera: EntityClientCamera) -> None:
        with self.database as db_session:
            db_session.add(client_camera.to_database_model())

    def get_client_camera_by_id(self, client_id: int) -> EntityClientCamera:
        with self.database as db_session:
            client_camera_model = db_session \
                .query(DatabaseMySQLModelClientCamera) \
                .filter(DatabaseMySQLModelClientCamera.client_id == client_id) \
                .first()
            if client_camera_model is None:
                raise Exception("Client camera not found in database")
            return EntityClientCamera(
                client_id=client_camera_model.client_id,
                camera_id=client_camera_model.camera_id,
                viewer_id=client_camera_model.viewer_id,
            )

