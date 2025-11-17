from database.models.person_image_path import DatabaseModelPersonImagePath
from entities.person_image_path import EntityPersonImagePath
import uuid
from errors.modules.database import ErrorModuleDatabase
from database import Database
from entities.database.where.person_image_paths import EntityDatabaseWherePersonImagePath
class ModuleDatabasePersonImagePaths:
    def __init__(self, database: Database):
        self.database = database

    def insert(self, person_image_path: EntityPersonImagePath) -> None:
        try:
            with self.database as db_session:
                db_session.add(person_image_path.to_database_model())
                db_session.commit()
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to insert person image path: {e}")

    def select_by_id(self, id: uuid.UUID) -> EntityPersonImagePath:
        try:
            with self.database as db_session:
                model = db_session.query(DatabaseModelPersonImagePath).filter(DatabaseModelPersonImagePath.image_id == id).first()
                if model is None:
                    raise ErrorModuleDatabase(f"Person image path with id {id} not found")
                return EntityPersonImagePath.from_database_model(model)
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to select person image path by id: {e}")

    def select(self, where: EntityDatabaseWherePersonImagePath) -> list[EntityPersonImagePath]:
        try:
            with self.database as db_session:
                query = db_session.query(DatabaseModelPersonImagePath)
                if where.after is not None:
                    query = query.filter(DatabaseModelPersonImagePath.timestamp >= where.after)
                if where.before is not None:
                    query = query.filter(DatabaseModelPersonImagePath.timestamp <= where.before)
                if where.view_ids is not None:
                    query = query.filter(DatabaseModelPersonImagePath.view_id.in_(where.view_ids))
                if where.camera_ids is not None:
                    query = query.filter(DatabaseModelPersonImagePath.camera_id.in_(where.camera_ids))
                if where.image_ids is not None:
                    query = query.filter(DatabaseModelPersonImagePath.image_id.in_(where.image_ids))
                return [EntityPersonImagePath.from_database_model(model) for model in query.all()]
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to select person image paths: {e}")

    def select_by_image_id(self, image_id: uuid.UUID) -> EntityPersonImagePath:
        try:
            with self.database as db_session:
                model = db_session.query(DatabaseModelPersonImagePath).filter(DatabaseModelPersonImagePath.image_id == image_id).first()
                if model is None:
                    raise ErrorModuleDatabase(f"Person image path with image id {image_id} not found")
                return EntityPersonImagePath.from_database_model(model)
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to select person image path by image id: {e}")

    def update_all(self, person_image_paths: list[EntityPersonImagePath]) -> None:
        try:
            with self.database as db_session:
                for person_image_path in person_image_paths:
                    db_session.merge(person_image_path.to_database_model())
                db_session.commit()
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to update all person image paths: {e}")
