from typing import List
from datetime import datetime
from entities.person_flow_weight import EntityPersonFlowWeight
from modules.person_flow.calculator import ModulePersonFlowCalculator
from modules.person_flow.weight.calculator import ModulePersonFlowWeightCalculator
from repositories.database.person_features import RepositoryDatabasePersonFeatures
from repositories.database.person_features import RepositoryDatabasePersonFeaturesFilters
from repositories.database import RepositoryDatabaseEngine
from entities.environment.postgresql import EntityEnvironmentPostgreSQL

class ApplicationPersonFlow:
    def __init__(
        self,
        database_person_features: RepositoryDatabasePersonFeatures,
        flow_calculator: ModulePersonFlowCalculator,
        weight_calculator: ModulePersonFlowWeightCalculator,
    ):
        self.database_person_features = database_person_features
        self.flow_calculator = flow_calculator
        self.weight_calculator = weight_calculator

    def process(self, after_timestamp: datetime | None, before_timestamp: datetime | None) -> List[EntityPersonFlowWeight]:
        person_features = self.database_person_features.find_all(
            filters=RepositoryDatabasePersonFeaturesFilters(
                timestamp_after=after_timestamp,
                timestamp_before=before_timestamp,
            )
        )
        person_flows = self.flow_calculator.calculate(person_features)
        return self.weight_calculator.calculate(person_flows)

    @staticmethod
    def create(environment_postgresql: EntityEnvironmentPostgreSQL) -> "ApplicationPersonFlow":
        return ApplicationPersonFlow(
            database_person_features=RepositoryDatabasePersonFeatures(
                database=RepositoryDatabaseEngine(
                    host=environment_postgresql.host,
                    port=environment_postgresql.port,
                    database=environment_postgresql.database,
                    user=environment_postgresql.user,
                    password=environment_postgresql.password,
                ),
            ),
            flow_calculator=ModulePersonFlowCalculator(),
            weight_calculator=ModulePersonFlowWeightCalculator(),
        )
