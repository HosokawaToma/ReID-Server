from PIL import Image
from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results
from entities.yolo.keypoints import EntityYoloKeypoints
from error import Error


class ModuleYoloPoseError(Error):
    pass

class ModuleYoloPose:
    def __init__(self):
        self.model = YOLO("./resources/models/yolo11x-pose.pt")

    def extract(self, frame: Image.Image) -> EntityYoloKeypoints:
        results = self.model(frame, verbose=False)
        result: Results = results[0]
        if result.keypoints is None:
            raise ModuleYoloPoseError("yolo pose keypoints is None")
        if len(result.keypoints) == 0:
            raise ModuleYoloPoseError("yolo pose keypoints is empty")
        xys = result.keypoints.xy[0].tolist()
        if len(xys) == 0:
            raise ModuleYoloPoseError("yolo pose keypoints is empty")
        confs = result.keypoints.conf
        if confs is None:
            raise ModuleYoloPoseError("yolo pose confidences is None")
        if len(confs) == 0:
            raise ModuleYoloPoseError("yolo pose confidences is empty")
        confs = confs.flatten().tolist()
        return EntityYoloKeypoints(keypoints=xys, confidences=confs)
