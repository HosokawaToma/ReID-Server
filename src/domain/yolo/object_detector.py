"""
YOLO 物体検出のドメインラッパー

画像から人物のバウンディングボックス列を抽出する。
"""
from dataclasses import dataclass
from ultralytics.engine.results import Results, Boxes
from domain.yolo.bounding_box import DomainYoloBoundingBox
from domain.yolo.bounding_box_sequence import DomainYoloBoundingBoxSequence
from domain.utils.base import DomainUtilsBase
from domain.image import DomainImage
from modules.yolo.object_detector import ModuleYoloObjectDetector


@dataclass(frozen=True)
class DomainYoloObjectDetector(DomainUtilsBase):
    """
    YOLO の物体検出結果（バウンディングボックス等）を保持するドメインモデル。
    """
    model: ModuleYoloObjectDetector

    def extract_person(self, image: DomainImage) -> DomainYoloBoundingBoxSequence:
        """
        画像から人物のバウンディングボックス列を抽出する。

        :param DomainImage image: 入力画像
        :return DomainYoloBoundingBoxSequence: 検出框の列
        """
        results = self.model.extract_person(
            image.image,
        )
        detections = []
        for result in results:
            if result.boxes is None:
                continue
            for box in result.boxes:
                xyxy = box.xyxy[0].cpu().numpy()
                x1 = float(xyxy[0])
                y1 = float(xyxy[1])
                x2 = float(xyxy[2])
                y2 = float(xyxy[3])
                conf = float(box.conf[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())
                detections.append(DomainYoloBoundingBox(
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2,
                    confidence=conf,
                    class_id=class_id,
                ))
        return DomainYoloBoundingBoxSequence(items=detections)
