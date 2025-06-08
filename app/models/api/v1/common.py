from datetime import datetime
from pydantic.main import BaseModel
from typing import List, Optional
from pydantic import Field, ConfigDict, field_validator
from camel_converter import to_camel
from enum import Enum


class FromAttrModel(BaseModel):
    """
    모델 래퍼
    """
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

