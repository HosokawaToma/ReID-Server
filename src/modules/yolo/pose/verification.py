from entities.yolo.keypoints import EntityYoloKeypoints

class ModuleYoloPoseVerification:
    def __init__(
        self,
        confidence_threshold: float = 0.75
    ):
        self.confidence_threshold = confidence_threshold

    def verify(self, keypoints: EntityYoloKeypoints) -> bool:
        if len(keypoints.keypoints) != 17:
            return False
        mean_confidence = sum(keypoints.confidences) / len(keypoints.keypoints)
        if mean_confidence < self.confidence_threshold:
            return False
        return True
