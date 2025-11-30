from entities.person.flow import EntityPersonFlow
import uuid

class SequencePersonFlows:
    def __init__(self, person_flows: list[EntityPersonFlow], person_id: uuid.UUID):
        self.person_flows = person_flows
        self.person_id = person_id

    def to_json(self) -> dict[str, list[dict[str, str]]]:
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
