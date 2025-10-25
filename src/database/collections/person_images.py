from pymilvus import utility, CollectionSchema, FieldSchema, DataType, Collection

class DatabaseCollectionsPersonImages:
    COLLECTION_NAME = "person_images"

    def __init__(self):
        self.fields = [
            FieldSchema(name="image_id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        ]
        self.schema = CollectionSchema(self.fields, "Person Images")
        self.collection = None

    def collection(self) -> bool:
        if not utility.has_collection(self.COLLECTION_NAME):
            self.collection = Collection(self.COLLECTION_NAME, self.schema)
            return True
        else:
            return False
