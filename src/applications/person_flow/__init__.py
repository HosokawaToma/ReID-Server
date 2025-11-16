from typing import List
from datetime import datetime
from entities.person_feature import EntityPersonFeature
from entities.person_flow_weight import EntityPersonFlowWeight
from modules.person_flow.calculator import ModulePersonFlowCalculator
from modules.person_flow.weight.calculator import ModulePersonFlowWeightCalculator
from modules.database.person_features import ModuleDatabasePersonFeatures
from database import Database
from entities.environment.postgresql import EntityEnvironmentPostgreSQL

class ApplicationPersonFlow:
    def __init__(
        self,
        database_person_features: ModuleDatabasePersonFeatures,
        flow_calculator: ModulePersonFlowCalculator,
        weight_calculator: ModulePersonFlowWeightCalculator,
    ):
        self.database_person_features = database_person_features
        self.flow_calculator = flow_calculator
        self.weight_calculator = weight_calculator

    def process(self, after_timestamp: datetime | None, before_timestamp: datetime | None) -> List[EntityPersonFlowWeight]:
        person_features = self.database_person_features.select_by_timestamp_range(
            after_timestamp=after_timestamp,
            before_timestamp=before_timestamp,
        )
        person_flows = self.flow_calculator.calculate(person_features)
        return self.weight_calculator.calculate(person_flows)

    @staticmethod
    def create(environment_postgresql: EntityEnvironmentPostgreSQL) -> "ApplicationPersonFlow":
        return ApplicationPersonFlow(
            database_person_features=ModuleDatabasePersonFeatures(
                database=Database(
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
