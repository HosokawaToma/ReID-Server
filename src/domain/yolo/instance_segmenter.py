from domain.yolo.mask import DomainYoloMask
from domain.yolo.mask_sequence import DomainYoloMaskSequence
from domain.image import DomainImage
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from modules.yolo.instance_segmenter import ModuleYoloInstanceSegmenter


@dataclass(frozen=True)
class DomainYoloInstanceSegmenter(DomainUtilsBase):
    """
    YOLOの個体推定のドメインモデル
    """
    model: ModuleYoloInstanceSegmenter

    def extract(self, image: DomainImage) -> DomainYoloMaskSequence:
        """
        画像からマスクを抽出します
        実装は公式ドキュメントを参照しています
        :param DomainImage image: 画像
        :return DomainYoloMaskSequence: マスクのシーケンス
        """
        results = self.model.extract(image.image)
        if results.masks is None:
            return DomainYoloMaskSequence(items=[])
        masks = []
        for mask in results.masks:
            masks.append(DomainYoloMask(mask.xy.pop()))
        return DomainYoloMaskSequence(items=masks)
