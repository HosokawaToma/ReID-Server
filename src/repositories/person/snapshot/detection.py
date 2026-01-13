from repositories.utils.database import RepositoryUtilDatabase
from domain.person.snapshot.detection import DomainPersonSnapshotDetection
from migration.models.person_snapshot_detections import MigrationModelPersonSnapshotDetection

class RepositoryPersonSnapshotDetection:
    def __init__(self, database: RepositoryUtilDatabase):
        self.database = database

    def _domain_to_model(self, detection: DomainPersonSnapshotDetection) -> MigrationModelPersonSnapshotDetection:
        return MigrationModelPersonSnapshotDetection(
            id=detection.id,
            person_snapshot_id=detection.person_snapshot_id,
            class_id=detection.class_id,
            confidence=detection.confidence,
            x=detection.x,
            y=detection.y,
        )

    def _model_to_domain(self, model: MigrationModelPersonSnapshotDetection) -> DomainPersonSnapshotDetection:
        return DomainPersonSnapshotDetection(
            id=model.id,
            person_snapshot_id=model.person_snapshot_id,
            class_id=model.class_id,
            confidence=model.confidence,
            x=model.x,
            y=model.y,
            width=model.width,
            height=model.height,
        )
