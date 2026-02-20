"""
ReID モデルモジュール

CLIP-ReID を用いて画像・カメラ・ビューから人物特徴量を抽出する。
"""
import os
from typing import Optional
import torch
from PIL import Image
from torchvision import transforms
from yacs.config import CfgNode

from modules.reid.clip_reid.config import cfg
from modules.reid.clip_reid.model.make_model_clipreid import make_model

CONFIG_FILE_PATH = os.path.join(os.path.dirname(
    __file__), "clip_reid/configs/person/vit_clipreid.yml")
OPTIONS = [
    "MODEL.SIE_CAMERA",
    "True",
    "MODEL.SIE_COE",
    "1.0",
    "MODEL.STRIDE_SIZE",
    "[12, 12]",
    "DATASETS.ROOT_DIR",
    "resources/dataset",
    "DATASETS.NAMES",
    "",
    "MODEL.PRETRAIN_PATH",
    "resources/models/jx_vit_base_p16_224-80ecf9dd.pth",
    "TEST.WEIGHT",
    "resources/models/Market1501_clipreid_12x12sie_ViT-B-16_60.pth"
]


class ModuleReIDModelError(Exception):
    """ReID モデル未初期化など、モデル利用時の例外。"""
    pass


class ModuleReIDModel:
    """
    ReID 特徴量抽出モデル。

    クラス変数でモデル・前処理・設定をキャッシュし、画像とカメラ・ビューから特徴量を返す。
    """
    _model: torch.nn.Module | None = None
    _transform: transforms.Compose | None = None
    _config: CfgNode | None = None

    def __init__(self) -> None:
        """未ロード時は設定を読み込み、モデルと前処理を初期化する。"""
        if ModuleReIDModel._model is None:
            cfg.merge_from_file(CONFIG_FILE_PATH)
            cfg.merge_from_list(OPTIONS)
            cfg.freeze()
            ModuleReIDModel._config = cfg
            os.environ['CUDA_VISIBLE_DEVICES'] = cfg.MODEL.DEVICE_ID
            num_classes = torch.tensor(751, dtype=torch.int64).to(
                ModuleReIDModel._config.MODEL.DEVICE)
            camera_num = torch.tensor(6, dtype=torch.int64).to(
                ModuleReIDModel._config.MODEL.DEVICE)
            view_num = torch.tensor(1, dtype=torch.int64).to(
                ModuleReIDModel._config.MODEL.DEVICE)
            model = make_model(ModuleReIDModel._config,
                               num_classes, camera_num, view_num)
            model.load_param(ModuleReIDModel._config.TEST.WEIGHT)
            model.eval()
            model.to(ModuleReIDModel._config.MODEL.DEVICE)
            ModuleReIDModel._model = model

            ModuleReIDModel._transform = transforms.Compose(
                [
                    transforms.Resize(ModuleReIDModel._config.INPUT.SIZE_TEST),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        mean=ModuleReIDModel._config.INPUT.PIXEL_MEAN,
                        std=ModuleReIDModel._config.INPUT.PIXEL_STD
                    )
                ]
            )

    def extract_feature(self, image: Image.Image, camera_id: int, view_id: int) -> torch.Tensor:
        """
        画像とカメラ・ビューから人物特徴量を抽出する。

        :param Image.Image image: 入力画像
        :param int camera_id: カメラID
        :param int view_id: ビューID
        :return torch.Tensor: 特徴量ベクトル
        :raises ModuleReIDModelError: モデルが未初期化の場合
        """
        if ModuleReIDModel._model is None or ModuleReIDModel._transform is None or ModuleReIDModel._config is None:
            raise ModuleReIDModelError("model is not initialized")

        image_tensor: torch.Tensor = ModuleReIDModel._transform(
            image)  # pyright: ignore[reportAssignmentType]
        image_tensor = image_tensor.unsqueeze(0).to(
            ModuleReIDModel._config.MODEL.DEVICE)
        camera_id_tensor: Optional[torch.Tensor] = None

        if ModuleReIDModel._config.MODEL.SIE_CAMERA:
            camera_id_tensor = torch.tensor(
                camera_id, dtype=torch.long).to(ModuleReIDModel._config.MODEL.DEVICE)
        view_id_tensor: Optional[torch.Tensor] = None

        if ModuleReIDModel._config.MODEL.SIE_VIEW:
            view_id_tensor = torch.tensor(
                view_id, dtype=torch.long).to(ModuleReIDModel._config.MODEL.DEVICE)
        with torch.no_grad():
            return ModuleReIDModel._model(image_tensor, cam_label=camera_id_tensor, view_label=view_id_tensor).squeeze()
