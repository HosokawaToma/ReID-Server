from PIL import Image
from application.identify_person.background_process.clip_reid.assign_id import ApplicationIdentifyPersonBackgroundProcessAssignId
from application.identify_person.background_process.clip_reid.clip_reid_model import ApplicationIdentifyPersonBackgroundProcessClipReIDModel


class ApplicationIdentifyPersonBackgroundProcessClipReID:
    def __init__(self):
        self.clip_reid_model = ApplicationIdentifyPersonBackgroundProcessClipReIDModel()
        self.assign_id = ApplicationIdentifyPersonBackgroundProcessAssignId()

    def identify(self, image: Image, camera_id: int = 0, view_id: int = 0) -> int:
        query_feature = self.clip_reid_model.extract_feature(
            image,
            camera_id,
            view_id,
        )
        return self.assign_id.assign(query_feature)
