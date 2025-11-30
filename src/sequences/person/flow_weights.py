from entities.person.flow_weight import EntityPersonFlowWeight

class SequencePersonFlowWeights:
    def __init__(self, item: list[EntityPersonFlowWeight]):
        self.item = item

    def to_json(self) -> dict[str, list[dict[str, str | int]]]:
        return {
            "weights":[
                {
                    "target_camera_id": str(item.target_camera_id),
                    "source_camera_id": str(item.source_camera_id),
                    "weight": item.weight,
                } for item in self.item
            ]
        }
