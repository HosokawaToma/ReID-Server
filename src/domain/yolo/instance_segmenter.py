from ultralytics.models.yolo import YOLO
from domain.yolo.mask import DomainYoloMask
from domain.yolo.mask_sequence import DomainYoloMaskSequence
from ultralytics.engine.results import Results
from domain.image import DomainImage
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainYoloInstanceSegmenter(DomainUtilsBase):
    """
    YOLOの個体推定のドメインモデル
    """
    model: YOLO

    def extract(self, image: DomainImage) -> DomainYoloMaskSequence:
        """
        画像からマスクを抽出します
        実装は公式ドキュメントを参照しています
        :param DomainImage image: 画像
        :return DomainYoloMaskSequence: マスクのシーケンス
        """
        results = self.model(image.image, classes=[0], verbose=False)
        items: Results = results[0]
        if items.masks is None:
            return DomainYoloMaskSequence(items=[])
        masks = []
        for mask in items.masks:
            masks.append(DomainYoloMask(mask.xy.pop()))
        return DomainYoloMaskSequence(items=masks)
