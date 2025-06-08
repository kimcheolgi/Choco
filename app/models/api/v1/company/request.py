from typing import Dict, List

from pydantic import Field
from app.models.api.v1.common import FromAttrModel


class TagName(FromAttrModel):
    """
    태그명
    """
    tag_name: Dict[str, str]


class NewCompanyRequest(FromAttrModel):
    """
    회사정보 요청용
    """
    company_name: Dict[str, str]
    tags: List[TagName]
