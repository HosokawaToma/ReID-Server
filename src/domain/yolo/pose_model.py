from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results
from domain.yolo.key_points import DomainYoloKeyPoints
from PIL import Image

class DomainYoloPoseModel:
    def __init__(self):
        self.model = YOLO("./resources/models/yolo11x-pose.pt")

    def _extract(self, image: Image.Image) -> list[DomainYoloKeyPoints]:
        results = self.model(image, verbose=False)
        items: Results = results[0]
        keypoints: list[DomainYoloKeyPoints] = []
        for item in items:
            if item.keypoints is None:
                continue
            xys = item.keypoints.xy[0].tolist()
            confs = item.keypoints.conf
            if confs is None:
                continue
            confs = confs.squeeze().tolist()
            keypoints.append(DomainYoloKeyPoints(
                xys=xys,
                confidences=confs,
            ))
        return keypoints

    def is_full_body(self, image: Image.Image) -> bool:
        key_points = self._extract(image)
        if len(key_points) != 1:
            return False
        if not key_points[0].is_confidence():
            return False
        return True
