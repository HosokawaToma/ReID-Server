"""
YOLOポーズ推定モジュール

画像から人体キーポイントを検出する。
"""
from typing import ClassVar
from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results
from PIL import Image


class ModuleYoloPoseEstimator:
    """
    YOLOポーズ推定を行うモジュールクラス。

    指定モデルで画像を推論し、検出結果（キーポイント等）を返す。
    """
    WEIGHTS_PATH: ClassVar[str] = "./resources/models/yolo11x-pose.pt"
    DEVICE: ClassVar[str] = "cuda"

    def __init__(self) -> None:
        """
        モデルをロードして初期化する。
        """
        self.model = YOLO(self.WEIGHTS_PATH)

    def extract(self, image: Image.Image) -> Results:
        """
        画像からポーズ（キーポイント）を検出する。

        :param Image.Image image: 入力画像
        :return Results: 1フレーム分の検出結果（キーポイント等）
        """
        results = self.model(image, device=self.DEVICE, verbose=False)
        items: Results = results[0]
        return items
