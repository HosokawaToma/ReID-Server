from typing import List
from entities.person_feature import EntityPersonFeature
from entities.person_flow import EntityPersonFlow

class ModulePersonFlowCalculator:
    def calculate(self, person_features: List[EntityPersonFeature]) -> List[EntityPersonFlow]:
        person_flows = []
        for i in range(len(person_features)):
            if i == 0:
                continue
            person_flows.append(EntityPersonFlow(
                source_camera_id=person_features[i - 1].camera_id,
                target_camera_id=person_features[i].camera_id,
                source_timestamp=person_features[i - 1].timestamp,
                target_timestamp=person_features[i].timestamp,
            ))
        return person_flows
