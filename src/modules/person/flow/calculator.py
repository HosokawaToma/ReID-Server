from sequences.person.snapshots import SequencePersonSnapshots
from sequences.person.flows import SequencePersonFlows
from entities.person.flow import EntityPersonFlow
from datetime import timedelta

class ModulePersonFlowCalculatorError(Exception):
    pass
class ModulePersonFlowCalculatorPersonIdNotSetError(ModulePersonFlowCalculatorError):
    pass
class ModulePersonFlowCalculatorLessThanTwoSnapshotsError(ModulePersonFlowCalculatorError):
    pass

class ModulePersonFlowCalculator:
    def __init__(self, interval: timedelta):
        self.interval = interval

    def calculate(self, person_snapshots: SequencePersonSnapshots) -> SequencePersonFlows:
        person_snapshots = person_snapshots.sorted_by_timestamp()
        if person_snapshots.person_id is None:
            raise ModulePersonFlowCalculatorPersonIdNotSetError
        if len(person_snapshots.person_snapshots) < 2:
            raise ModulePersonFlowCalculatorLessThanTwoSnapshotsError
        person_flows = []
        for i in range(len(person_snapshots.person_snapshots)):
            if i == 0:
                continue
            if person_snapshots.person_snapshots[i].timestamp - person_snapshots.person_snapshots[i - 1].timestamp > self.interval:
                continue
            person_flows.append(
                EntityPersonFlow(
                    person_id=person_snapshots.person_id,
                    source_camera_id=person_snapshots.person_snapshots[i - 1].camera_id,
                    target_camera_id=person_snapshots.person_snapshots[i].camera_id,
                    source_timestamp=person_snapshots.person_snapshots[i - 1].timestamp,
                    target_timestamp=person_snapshots.person_snapshots[i].timestamp,
                )
            )
        return SequencePersonFlows(person_flows=person_flows, person_id=person_snapshots.person_id)
