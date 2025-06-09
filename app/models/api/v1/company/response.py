from typing import List

from pydantic import Field
from app.models.api.v1.common import FromAttrModel


class AutoCompleteCompanyResponse(FromAttrModel):
    """
    자동완성 회사명 데이터
    """
    company_name: str = Field(title="회사명")


class AutoCompleteCompanyListResponse(FromAttrModel):
    """
    회사명 리스트
    """
    data: List[AutoCompleteCompanyResponse] = Field(title="회사명 리스트")


class CompanyDetailResponse(FromAttrModel):
    """
    회사 데이터
    """
    company_name: str = Field(title="회사명")
    tags: List[str] = Field(title="태그 리스트")


class CompanyDetailDataResponse(FromAttrModel):
    """
    회사 데이터 래퍼
    """
    data: CompanyDetailResponse = Field(title="회사 상세 데이터")


class CompanyResponse(FromAttrModel):
    """
    회사 정보 반환용
    """
    company_name: str = Field(title="회사명")
    tags: List[str] = Field(title="태그 리스트")


class CompanyItemResponse(FromAttrModel):
    """
    회사명
    """
    company_name: str = Field(title="회사명")


class CompanyItemListResponse(FromAttrModel):
    """
    회사명 리스트
    """
    data: List[CompanyItemResponse] = Field(title="회사명 리스트")