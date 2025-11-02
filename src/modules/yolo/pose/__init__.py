from PIL import Image
from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results
from entities.yolo.keypoints import EntityYoloKeypoints


class ModuleYoloPose:
    def __init__(self):
        self.model = YOLO("models/yolo11x-pose.pt")

    def extract(self, frame: Image.Image) -> EntityYoloKeypoints | None:
        results = self.model(frame, verbose=False)
        result: Results = results[0]
        if result.keypoints is None:
            return None
        if len(result.keypoints) == 0:
            return None
        xys = result.keypoints.xy[0].tolist()
        confs = result.keypoints.conf
        if confs is None:
            return None
        confs = confs.tolist()
        return EntityYoloKeypoints(keypoints=xys, confidences=confs)
