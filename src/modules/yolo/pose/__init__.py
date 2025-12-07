from PIL import Image
from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results
from entities.yolo.keypoints import EntityYoloKeypoints

class ModuleYoloPose:
    def __init__(self):
        self.model = YOLO("./resources/models/yolo11x-pose.pt")

    def extract(self, frame: Image.Image) -> list[EntityYoloKeypoints] | None:
        results = self.model(frame, verbose=False)
        items: Results = results[0]
        keypoints: list[EntityYoloKeypoints] = []
        for item in items:
            if item.keypoints is None:
                continue
            xys = item.keypoints.xy.tolist()
            confs = item.keypoints.conf
            if confs is None:
                continue
            confs = confs.squeeze().tolist()
            keypoints.append(EntityYoloKeypoints(keypoints=xys, confidences=confs))
        return keypoints
