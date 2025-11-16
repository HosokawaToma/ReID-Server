from typing import Dict, List, Tuple
from entities.person_flow import EntityPersonFlow
from entities.person_flow_weight import EntityPersonFlowWeight

class ModulePersonFlowWeightCalculator:
    def calculate(self, person_flows: List[EntityPersonFlow]) -> List[EntityPersonFlowWeight]:
        person_flow_weights_dict: Dict[Tuple[int, int], float] = {}
        for person_flow in person_flows:
            if not (person_flow.source_camera_id, person_flow.target_camera_id) in person_flow_weights_dict:
                person_flow_weights_dict[(person_flow.source_camera_id, person_flow.target_camera_id)] = 0.0
            person_flow_weights_dict[(person_flow.source_camera_id, person_flow.target_camera_id)] += 1.0
        person_flow_weights = []
        for (source_camera_id, target_camera_id), weight in person_flow_weights_dict.items():
            person_flow_weights.append(EntityPersonFlowWeight(
                source_camera_id=source_camera_id,
                target_camera_id=target_camera_id,
                weight=weight,
            ))
        return person_flow_weights
