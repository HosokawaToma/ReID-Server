from repositories import RepositoryDatabase
from domain.person.snapshot.answer_only import DomainPersonSnapshotAnswerOnly
from domain.person.snapshot.person_id_value import DomainPersonSnapshotPersonIdValue
from domain.id_value import DomainIdValue
from migration.models.person_snapshot_answers import MigrationModelPersonSnapshotAnswer
from environment import Environment
from error import Error



class RepositoryPersonSnapshotAnswerOnlyError(Error):
    pass


class RepositoryPersonSnapshotAnswerOnlySaveError(RepositoryPersonSnapshotAnswerOnlyError):
    pass


class RepositoryPersonSnapshotAnswerOnly:
    def __init__(self, database: RepositoryDatabase):
        self.database = database

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshotAnswerOnly":
        return cls(
            database=RepositoryDatabase.create(environment),
        )

    def _model_to_domain(self, model: MigrationModelPersonSnapshotAnswer) -> DomainPersonSnapshotAnswerOnly:
        return DomainPersonSnapshotAnswerOnly(
            id=DomainIdValue(id=model.person_snapshot_id),
            answer=DomainPersonSnapshotPersonIdValue(
                person_id=DomainIdValue(id=model.person_id),
                is_junk=model.is_junk,
            ),
        )

    def _domain_to_model(self, domain: DomainPersonSnapshotAnswerOnly) -> MigrationModelPersonSnapshotAnswer:
        return MigrationModelPersonSnapshotAnswer(
            id=domain.id.id,
            person_id=domain.answer.person_id,
            is_junk=domain.answer.is_junk,
        )

    def save(self, answer: DomainPersonSnapshotAnswerOnly) -> None:
        try:
            with self.database as session:
                session.add(self._domain_to_model(answer))
        except Error as error:
            raise RepositoryPersonSnapshotAnswerOnlySaveError(error) from error
