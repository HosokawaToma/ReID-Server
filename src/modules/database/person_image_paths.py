from database.models.person_image_path import DatabaseModelPersonImagePath
from entities.person_image_path import EntityPersonImagePath
import uuid
from errors.modules.database import ErrorModuleDatabase
from database import Database

class ModuleDatabasePersonImagePaths:
    def __init__(self, database: Database):
        self.database = database

    def insert(self, person_image_path: EntityPersonImagePath) -> None:
        with self.database as db_session:
            db_session.add(person_image_path.to_database_model())
            db_session.commit()

    def select_by_id(self, id: uuid.UUID) -> EntityPersonImagePath:
        with self.database as db_session:
            model = db_session.query(DatabaseModelPersonImagePath).filter(DatabaseModelPersonImagePath.image_id == id).first()
            if model is None:
                raise ErrorModuleDatabase(f"Person image path with id {id} not found")
            return EntityPersonImagePath.from_database_model(model)

    def update_all(self, person_image_paths: list[EntityPersonImagePath]) -> None:
        with self.database as db_session:
            for person_image_path in person_image_paths:
                db_session.merge(person_image_path.to_database_model())
            db_session.commit()
