from dataclasses import dataclass
from domain.image import DomainImage
from domain.location import DomainLocation
from domain.person.feature import DomainPersonFeature
from domain.utils.base import DomainUtilsBase
from modules.reid.model import ModuleReIDModel

@dataclass
class DomainReIDModel(DomainUtilsBase):
    def __init__(self, model: ModuleReIDModel):
        self.model = model

    def extract(self, image: DomainImage, location: DomainLocation) -> DomainPersonFeature:
        return DomainPersonFeature(
            feature=self.model.extract_feature(
                image=image.image,
                camera_id=location.camera_id,
                view_id=location.view_id,
            ),
        )
