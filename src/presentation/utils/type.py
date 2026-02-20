"""
プレゼンテーション用型エイリアス

FastAPI の Form / Path / Depends で用いる Annotated 型を定義する。
"""
from fastapi import Depends
from dto.image import DtoImage
from presentation.utils.factory import PresentationUtilFactoryFromImage
from datetime import datetime
from fastapi import Form, Path
from typing import Annotated
import uuid

PresentationUtilFromImage = Annotated[DtoImage, Depends(
    PresentationUtilFactoryFromImage())]

PresentationUtilFromDatetime = Annotated[datetime, Form(...)]

PresentationUtilPathTimestamp = Annotated[datetime, Path(...)]

PresentationUtilPathDate = Annotated[datetime, Path(...)]

PresentationUtilPathUUID = Annotated[uuid.UUID, Path(...)]

PresentationUtilFromInt = Annotated[int, Form(...)]

PresentationUtilPathInt = Annotated[int, Path(...)]
