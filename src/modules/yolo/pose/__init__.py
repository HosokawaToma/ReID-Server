from PIL import Image
from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results
from entities.yolo.keypoints import EntityYoloKeypoints
from errors.modules.yolo.pose import ErrorModuleYoloPose

class ModuleYoloPose:
    def __init__(self):
        self.model = YOLO("./resources/models/yolo11x-pose.pt")

    def extract(self, frame: Image.Image) -> EntityYoloKeypoints | None:
        try:
            results = self.model(frame, verbose=False)
        except Exception as e:
            raise ErrorModuleYoloPose(f"Failed to extract keypoints: {e}")
        result: Results = results[0]
        if result.keypoints is None:
            return None
        if len(result.keypoints) == 0:
            return None
        xys = result.keypoints.xy[0].tolist()
        confs = result.keypoints.conf
        if confs is None:
            return None
        confs = confs.squeeze().tolist()
        return EntityYoloKeypoints(keypoints=xys, confidences=confs)
