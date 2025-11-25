import torch

class ModuleReIDIdentifierError(Exception):
    pass

class ModuleReIDIdentifier:
    def __init__(self, threshold: float):
        self.threshold = threshold

    def guarantee(self, query_feature: torch.Tensor, gallery_feature: torch.Tensor) -> None:
        if gallery_feature.device != query_feature.device:
            gallery_feature = gallery_feature.to(query_feature.device)
        if not torch.nn.functional.cosine_similarity(query_feature, gallery_feature, dim=0).item() > self.threshold:
            raise ModuleReIDIdentifierError
