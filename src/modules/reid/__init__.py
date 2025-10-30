from PIL import Image
from modules.reid.assigner import ModuleReIDAssigner
from modules.reid.model import ModuleReIDModel


class ModuleReID:
    def __init__(
        self,
        model: ModuleReIDModel,
        assigner: ModuleReIDAssigner,
    ):
        self.model = model
        self.assigner = assigner

    def identify(self, image: Image, camera_id: int = 0, view_id: int = 0) -> int:
        query_feature = self.model.extract_feature(
            image,
            camera_id,
            view_id,
        )
        return self.assigner.assign(query_feature)
