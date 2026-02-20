"""
ReID 同一人物判定モジュール

コサイン類似度と閾値で同一人物かどうかを判定する。
"""
import torch


class ModuleReIDIdentifier:
    """
    特徴量のコサイン類似度が閾値以上なら同一人物とみなす識別器。
    """

    def __init__(self, threshold: float) -> None:
        """
        閾値を設定して初期化する。

        :param float threshold: 同一人物とみなす類似度の閾値
        """
        self.threshold = threshold

    def identify(self, query_feature: torch.Tensor, gallery_feature: torch.Tensor) -> bool:
        """
        クエリとギャラリーの特徴量が同一人物かどうかを返す。

        :param torch.Tensor query_feature: クエリ特徴量
        :param torch.Tensor gallery_feature: ギャラリー特徴量
        :return bool: 同一人物とみなす場合 True
        """
        if gallery_feature.device != query_feature.device:
            gallery_feature = gallery_feature.to(query_feature.device)
        return torch.nn.functional.cosine_similarity(query_feature, gallery_feature, dim=0).item() > self.threshold
