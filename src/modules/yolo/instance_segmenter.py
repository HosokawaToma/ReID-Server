"""
YOLOインスタンスセグメンテーションモジュール

画像からインスタンスセグメンテーション（マスク）を取得する。
"""
from typing import ClassVar
from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results
from PIL import Image


class ModuleYoloInstanceSegmenter:
    """
    YOLOインスタンスセグメンテーションを行うモジュールクラス。

    画像を推論し、1フレーム分の検出結果（マスク等）を返す。
    """
    WEIGHTS_PATH: ClassVar[str] = "./resources/models/yolo11x-seg.pt"
    DEVICE: ClassVar[str] = "cuda"

    def __init__(self) -> None:
        """
        モデルをロードして初期化する。
        """
        self.model = YOLO(self.WEIGHTS_PATH)

    def extract(self, image: Image.Image) -> Results:
        """
        画像からインスタンスセグメンテーション（マスク）を検出する。

        :param Image.Image image: 入力画像
        :return Results: 1フレーム分の検出結果（マスク等）
        """
        results = self.model(image, device=self.DEVICE, verbose=False)
        return results[0]
