"""
YOLO物体検出モジュール

画像から人物を検出する。
"""
from typing import ClassVar
from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results
from PIL import Image


class ModuleYoloObjectDetector:
    """
    YOLO物体検出を行うモジュールクラス。

    人物クラスのみを対象に検出し、フレームごとの検出結果リストを返す。
    """
    WEIGHTS_PATH: ClassVar[str] = "./resources/models/yolo11x.pt"
    PERSON_CLASS: ClassVar[int] = 0
    IOU_THRESHOLD: ClassVar[float] = 0.5
    CONFIDENCE_THRESHOLD: ClassVar[float] = 0.5
    DEVICE: ClassVar[str] = "cuda"

    def __init__(self) -> None:
        """
        モデルをロードして初期化する。
        """
        self.model = YOLO(self.WEIGHTS_PATH)

    def extract_person(self, image: Image.Image) -> list[Results]:
        """
        画像から人物を検出する。人物クラスのみを対象とする。

        :param Image.Image image: 入力画像
        :return list[Results]: フレームごとの検出結果のリスト
        """
        results = self.model(
            image,
            classes=[self.PERSON_CLASS],
            iou=self.IOU_THRESHOLD,
            conf=self.CONFIDENCE_THRESHOLD,
            device=self.DEVICE,
            verbose=False,
        )
        return results
