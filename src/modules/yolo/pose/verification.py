from entities.yolo.keypoints import EntityYoloKeypoints

class ModuleYoloPoseVerification:
    def __init__(
        self,
        confidence_threshold: float = 0.75
    ):
        self.confidence_threshold = confidence_threshold

    def verify(self, keypoints: list[EntityYoloKeypoints]) -> bool:
        if len(keypoints) != 1:
            return False
        if len(keypoints[0].keypoints) != 17:
            return False
        mean_confidence = sum(keypoints[0].confidences) / len(keypoints[0].keypoints)
        if mean_confidence < self.confidence_threshold:
            return False
        return True
