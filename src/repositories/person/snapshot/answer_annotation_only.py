from repositories import RepositoryDatabase
from domain.person.snapshot.answer_annotation_only import DomainPersonSnapshotAnswerAnnotationOnly
from domain.person.snapshot.answer_annotation_only_sequence import DomainPersonSnapshotAnswerAnnotationOnlySequence
from value.person.snapshot.annotation import ValuePersonSnapshotAnnotation
from value.id import ValueId
from migration.models.person_snapshot_answer_annotations import MigrationModelPersonSnapshotAnswerAnnotation
from environment import Environment
from error import Error



class RepositoryPersonSnapshotAnswerAnnotationOnlyError(Error):
    pass


class RepositoryPersonSnapshotAnswerAnnotationOnlySaveError(RepositoryPersonSnapshotAnswerAnnotationOnlyError):
    pass


class RepositoryPersonSnapshotAnswerAnnotationOnly:
    def __init__(self, database: RepositoryDatabase):
        self.database = database

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshotAnswerAnnotationOnly":
        return cls(
            database=RepositoryDatabase.create(environment),
        )

    def _model_to_domain(self, model: MigrationModelPersonSnapshotAnswerAnnotation) -> DomainPersonSnapshotAnswerAnnotationOnly:
        return DomainPersonSnapshotAnswerAnnotationOnly(
            id=ValueId(id=model.person_snapshot_id),
            answer=ValuePersonSnapshotAnnotation(
                _person_id=ValueId(id=model.person_id),
                _is_junk=model.is_junk,
            ),
        )

    def _domain_to_model(self, domain: DomainPersonSnapshotAnswerAnnotationOnly) -> MigrationModelPersonSnapshotAnswerAnnotation:
        return MigrationModelPersonSnapshotAnswerAnnotation(
            person_snapshot_id=domain.id.id,
            person_id=domain.answer.person_id.id if domain.answer.person_id is not None else None,
            is_junk=domain.answer.is_junk,
        )

    def save_all(self, answer_annotations: DomainPersonSnapshotAnswerAnnotationOnlySequence) -> None:
        try:
            with self.database as session:
                session.add_all(
                    [
                        self._domain_to_model(answer_annotation)
                        for answer_annotation in answer_annotations
                    ],
                )
        except Error as error:
            raise RepositoryPersonSnapshotAnswerAnnotationOnlySaveError(error) from error
