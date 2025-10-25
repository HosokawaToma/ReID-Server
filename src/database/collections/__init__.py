from database.collections.person_images import DatabaseCollectionsPersonImages

class DatabaseCollections:
    def __init__(
        self,
        person_images: DatabaseCollectionsPersonImages,
        ):
        self.person_images = person_images

    @staticmethod
    def create():
        return DatabaseCollections(
            person_images=DatabaseCollectionsPersonImages(),
        )
