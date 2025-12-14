class DomainYoloKeyPoints:
    confidence_threshold: float = 0.75

    def __init__(self, xys: list[tuple[float, float]], confidences: list[float]):
        self.xys = xys
        self.confidences = confidences

    def is_confidence(self) -> bool:
        if len(self.confidences) != 17:
            return False
        mean_confidence = sum(self.confidences) / len(self.confidences)
        if mean_confidence < self.confidence_threshold:
            return False
        return True
