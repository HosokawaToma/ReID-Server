from entities.person.flow import EntityPersonFlow
from entities.person.flow_weight import EntityPersonFlowWeight
from sequences.person.flow_weights import SequencePersonFlowWeights
import uuid

class SequencePersonFlowsError(Exception):
    pass
class SequencePersonFlowsPersonIdNotSetError(SequencePersonFlowsError):
    pass

class SequencePersonFlows:
    @property
    def person_id(self) -> uuid.UUID | None:
        if len(self.person_flows) == 0:
            return None
        for i in range(len(self.person_flows)):
            if i == 0:
                continue
            if self.person_flows[i].person_id != self.person_flows[i - 1].person_id:
                return None
        return self.person_flows[0].person_id

    def __init__(self, person_flows: list[EntityPersonFlow], person_id: uuid.UUID | None = None):
        self.person_flows = person_flows

    @classmethod
    def combine(cls, sequences: list["SequencePersonFlows"]) -> "SequencePersonFlows":
        person_flows = []
        for sequence in sequences:
            person_flows.extend(sequence.person_flows)
        return cls(person_flows=person_flows)

    def convert_to_weights(self) -> SequencePersonFlowWeights:
        weights: dict[tuple[int, int], int] = {}
        for item in self.person_flows:
            key = (item.source_camera_id, item.target_camera_id)
            if weights.get(key) is None:
                weights[key] = 0
            weights[key] += 1
        return SequencePersonFlowWeights(
            item=[
                EntityPersonFlowWeight(
                    target_camera_id=target_camera_id,
                    source_camera_id=source_camera_id,
                    weight=weight,
                ) for (source_camera_id, target_camera_id), weight in weights.items()
            ]
        )

    def to_json(self) -> dict[str, list[dict[str, str]]]:
        if self.person_id is None:
            raise SequencePersonFlowsPersonIdNotSetError
        return {
            str(self.person_id): [
                {
                    "source_camera_id": str(person_flow.source_camera_id),
                    "target_camera_id": str(person_flow.target_camera_id),
                    "source_timestamp": person_flow.source_timestamp.isoformat(),
                    "target_timestamp": person_flow.target_timestamp.isoformat(),
                } for person_flow in self.person_flows
            ]
        }
