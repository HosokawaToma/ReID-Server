import torch

class ModuleReIDIdentifier:
    def __init__(self, threshold: float):
        self.threshold = threshold

    def identify(self, query_feature: torch.Tensor, gallery_feature: torch.Tensor) -> bool:
        if gallery_feature.device != query_feature.device:
            gallery_feature = gallery_feature.to(query_feature.device)
        return torch.nn.functional.cosine_similarity(query_feature, gallery_feature, dim=0).item() > self.threshold
