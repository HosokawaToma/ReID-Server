from ultralytics.models.yolo import YOLO
from domain.yolo.mask import DomainYoloMask
from domain.yolo.mask_sequence import DomainYoloMaskSequence
from ultralytics.engine.results import Results
from PIL import Image
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainYoloInstanceSegmenter(DomainUtilsBase):
    """
    YOLOの個体推定のドメインモデル
    """
    model: YOLO

    def extract(self, image: Image.Image) -> DomainYoloMaskSequence:
        """
        画像からマスクを抽出します
        実装内容は公式ドキュメントを参照
        :param DomainImage image: 画像
        :return DomainYoloMaskSequence: マスクのシーケンス
        """
        results = self.model(image, classes=[0], verbose=False)
        items: Results = results[0]
        if items.masks is None:
            return DomainYoloMaskSequence(items=[])
        masks = []
        for mask in items.masks:
            masks.append(DomainYoloMask(mask.xy.pop()))
        return DomainYoloMaskSequence(items=masks)
