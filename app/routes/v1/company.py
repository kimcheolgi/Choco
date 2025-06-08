from typing import List

from fastapi import APIRouter, status, Depends, Form, UploadFile, File, Request, Body, Query, Header, Path

from sqlalchemy.orm import Session
from app.database.conn_sqlalchemy import db
from app.models.api.v1.company.request import NewCompanyRequest, TagName
from app.models.api.v1.company.response import AutoCompleteCompanyListResponse, CompanyDetailDataResponse, \
    CompanyResponse, CompanyItemListResponse
from app.services.api.v1.company import get_autocomplete_company_name, get_company_detail, create_company, \
    search_company_by_tag_name, add_tags_to_company, delete_company_tag

from app.utils.parse_utils import generate_error_responses

router = APIRouter(prefix='')


@router.get(
    path="/search",
    response_model=AutoCompleteCompanyListResponse,
    responses=generate_error_responses("ERR50001"),
    status_code=status.HTTP_200_OK
)
def api_get_autocomplete_company(
    query: str = Query(..., min_length=1),
    x_wanted_language: str = Header(default="ko"),
    session: Session = Depends(db.get_writer_db)
) -> AutoCompleteCompanyListResponse:

    return get_autocomplete_company_name(query=query, language_code=x_wanted_language, session=session)


@router.get(
    path="/companies/{company_name}",
    response_model=CompanyDetailDataResponse,
    responses=generate_error_responses("ERR50001", "ERR40401"),
    status_code=status.HTTP_200_OK
)
def api_get_company_detail(
    company_name: str,
    x_wanted_language: str = Header(default="ko"),
    session: Session = Depends(db.get_writer_db)
) -> CompanyDetailDataResponse:

    return get_company_detail(
        company_name=company_name,
        language_code=x_wanted_language,
        session=session
    )


@router.post(
    "/companies",
    response_model=CompanyResponse,
    responses=generate_error_responses("ERR50001", "ERR40001"),
    status_code=status.HTTP_200_OK
)
def api_create_company(
    body: NewCompanyRequest,
    x_wanted_language: str = Header(default="ko"),
    session: Session = Depends(db.get_writer_db)
) -> CompanyResponse:
    return create_company(
        body=body,
        language_code=x_wanted_language,
        session=session
    )


@router.get(
    "/tags",
    response_model=CompanyItemListResponse,
    responses=generate_error_responses("ERR50001", "ERR40401"),
    status_code=status.HTTP_200_OK
)
def api_search_company_by_tag_name(
    query: str = Query(..., min_length=1),
    x_wanted_language: str = Header(default="ko"),
    session: Session = Depends(db.get_writer_db)
):
    return search_company_by_tag_name(
        query=query,
        language_code=x_wanted_language,
        session=session
    )


@router.put(
    "/companies/{company_name}/tags",
    response_model=CompanyResponse,
    responses=generate_error_responses("ERR50001", "ERR40401", "ERR40001"),
    status_code=status.HTTP_200_OK
)
def api_add_tags_to_company(
    company_name: str = Path(...),
    tags: List[TagName] = [],
    x_wanted_language: str = Header(default="ko"),
    session: Session = Depends(db.get_writer_db)
) -> CompanyResponse:
    return add_tags_to_company(
        company_name=company_name,
        tags=tags,
        language_code=x_wanted_language,
        session=session
    )


@router.delete(
    "/companies/{company_name}/tags/{tag_name}",
    response_model=CompanyResponse,
    responses=generate_error_responses("ERR50001", "ERR40401"),
    status_code=status.HTTP_200_OK
)
def api_delete_company_tag(
    company_name: str = Path(...),
    tag_name: str = Path(...),
    x_wanted_language: str = Header(default="ko"),
    session: Session = Depends(db.get_writer_db)
) -> CompanyResponse:
    return delete_company_tag(
        company_name=company_name,
        tag_name=tag_name,
        language_code=x_wanted_language,
        session=session
    )