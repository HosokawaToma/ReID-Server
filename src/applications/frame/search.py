from repositories.frame_image import RepositoryFrameImage
from domain.frame_image.filter import DomainFrameImageFilter
from domain.frame_image.ordering import DomainFrameImageOrdering
from dto.frame_image.meta_data import DtoFrameImageMetaData
from dto.frame_image.filter import DtoFrameImageFilter
from dto.frame_image.ordering import DtoFrameImageOrdering
from environment import Environment

class ApplicationFrameSearch:
    def __init__(self, repository_frame_image: RepositoryFrameImage):
        self.repository_frame_image = repository_frame_image

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationFrameSearch":
        return cls(
            repository_frame_image=RepositoryFrameImage.create(environment),
        )

    def search(self, filters: DtoFrameImageFilter | None = None, ordering: DtoFrameImageOrdering | None = None) -> list[DtoFrameImageMetaData]:
        filters_domain = None
        if filters is not None:
            filters_domain = DomainFrameImageFilter.from_dto(filters)
        ordering_domain = None
        if ordering is not None:
            ordering_domain = DomainFrameImageOrdering.from_dto(ordering)
        meta_data_list = self.repository_frame_image.meta_data_find_all(
            filters=filters_domain,
            ordering=ordering_domain,
        )
        return [DtoFrameImageMetaData(
            id=meta_data.id,
            camera_id=meta_data.camera_id,
            view_id=meta_data.view_id,
            timestamp=meta_data.timestamp,
        ) for meta_data in meta_data_list]
