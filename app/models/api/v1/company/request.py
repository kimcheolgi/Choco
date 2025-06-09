from typing import Dict, List

from pydantic import Field
from app.models.api.v1.common import FromAttrModel


class TagName(FromAttrModel):
    """
    태그명
    """
    tag_name: Dict[str, str] = Field(title="태그 정보")


class NewCompanyRequest(FromAttrModel):
    """
    회사정보 요청용
    """
    company_name: Dict[str, str] = Field(title="회사명 정보")
    tags: List[TagName] = Field(title="태그 정보 리스트")
