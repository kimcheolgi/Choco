from typing import List

from sqlalchemy import select, distinct, delete
from sqlalchemy.orm import Session
from app.database.schema.company import CompanyTranslation, CompanyTag, TagGroupTranslation, Company, TagGroup
from app.errors.exceptions import NotFoundEx, BadRequestEx
from app.models.api.v1.company.request import NewCompanyRequest, TagName
from app.models.api.v1.company.response import AutoCompleteCompanyListResponse, AutoCompleteCompanyResponse, \
    CompanyDetailDataResponse, CompanyDetailResponse, CompanyResponse, CompanyItemResponse, CompanyItemListResponse


def get_autocomplete_company_name(
    query: str,
    language_code: str,
    session: Session
) -> AutoCompleteCompanyListResponse:
    """
    회사명 자동완성
    회사명의 일부만 들어가도 검색
    header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    """
    stmt = (
        select(
            CompanyTranslation.name.label("company_name"),
        ).where(
            CompanyTranslation.name.ilike(f"%{query}%"),
            CompanyTranslation.language_code == language_code
        )
    )
    results = session.execute(stmt).all()

    return AutoCompleteCompanyListResponse(
        data=[
            AutoCompleteCompanyResponse.from_orm(
                result
            ) for result in results
        ]
    )


def get_company_detail(
    company_name: str,
    language_code: str,
    session: Session
) -> CompanyDetailDataResponse:
    """
    회사 이름으로 회사 검색
    header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    데이터가 없으면 404에러 발생
    """
    stmt = (
        select(
            CompanyTranslation
        ).where(
            CompanyTranslation.name == company_name
        ).where(
            CompanyTranslation.language_code == language_code
        )
    )
    company_translation = session.execute(stmt).scalar_one_or_none()

    if not company_translation:
        raise NotFoundEx(code="ERR40401")

    stmt_tags = (
        select(
            CompanyTag.tag_group_id
        ).where(
            CompanyTag.company_id == company_translation.company_id
        )
    )
    tag_ids = session.execute(stmt_tags).scalars().all()

    if tag_ids:
        stmt_tag_names = (
            select(
                TagGroupTranslation
            ).where(
                TagGroupTranslation.tag_group_id.in_(tag_ids)
            ).where(
                TagGroupTranslation.language_code == language_code
            )
        )
        tag_translations = session.execute(stmt_tag_names).scalars().all()
        tags = [t.name for t in tag_translations]
    else:
        tags = []

    return CompanyDetailDataResponse(
        data=CompanyDetailResponse(
            company_name=company_translation.name,
            tags=tags
        )
    )


def create_company(
    body: NewCompanyRequest,
    language_code: str,
    session: Session
) -> CompanyResponse:
    """
    새로운 회사 추가
    새로운 언어(tw)도 같이 추가 될 수 있음
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    """
    new_company = Company()
    session.add(new_company)
    session.flush()

    for lang, name in body.company_name.items():
        session.add(
            CompanyTranslation(
                company_id=new_company.id,
                language_code=lang,
                name=name
            )
        )

    for tag in body.tags:
        base_name = tag.tag_name.get("ko") or next(iter(tag.tag_name.values()))
        try:
            tag_id = int("".join(filter(str.isdigit, base_name)))
        except:
            raise BadRequestEx(code="ERR40001")

        tag_group = session.get(TagGroup, tag_id)
        if not tag_group:
            tag_group = TagGroup(id=tag_id)
            session.add(tag_group)
            session.flush()

        for lang, tag_name in tag.tag_name.items():
            exists = session.scalar(
                select(TagGroupTranslation)
                .where(TagGroupTranslation.tag_group_id == tag_id)
                .where(TagGroupTranslation.language_code == lang)
            )
            if not exists:
                session.add(TagGroupTranslation(
                    tag_group_id=tag_id,
                    language_code=lang,
                    name=tag_name
                ))

        session.add(CompanyTag(company_id=new_company.id, tag_group_id=tag_id))

    session.commit()

    name_translation = session.scalar(
        select(
            CompanyTranslation.name
        ).where(
            CompanyTranslation.company_id == new_company.id
        ).where(
            CompanyTranslation.language_code == language_code
        )
    )

    tag_names = session.scalars(
        select(
            TagGroupTranslation.name
        ).join(
            CompanyTag,
            TagGroupTranslation.tag_group_id == CompanyTag.tag_group_id
        ).where(
            CompanyTag.company_id == new_company.id
        ).where(
            TagGroupTranslation.language_code == language_code
        )
    ).all()
    return CompanyResponse(
        company_name=name_translation,
        tags=tag_names
    )


def search_company_by_tag_name(
    query: str,
    language_code: str,
    session: Session
) -> CompanyItemListResponse:
    """
    태그명으로 회사 검색
    태그로 검색 관련된 회사 검색
    다국어로 검색 가능
    일본어 태그로 검색을 해도 language가 ko이면 한국 회사명이 노출
    ko언어가 없을경우 노출가능한 언어로 출력
    동일한 회사는 한번만 노출
    """
    tag_translation_stmt = (
        select(TagGroupTranslation.tag_group_id)
        .where(TagGroupTranslation.name == query)
    )
    tag_group_ids = session.execute(tag_translation_stmt).scalars().all()
    if not tag_group_ids:
        return CompanyItemListResponse(data=[])

    company_ids_stmt = (
        select(distinct(CompanyTag.company_id))
        .where(CompanyTag.tag_group_id.in_(tag_group_ids))
    )
    company_ids = session.execute(company_ids_stmt).scalars().all()
    if not company_ids:
        return CompanyItemListResponse(data=[])

    results = []
    for company_id in company_ids:
        company_name = session.scalar(
            select(CompanyTranslation.name)
            .where(CompanyTranslation.company_id == company_id)
            .where(CompanyTranslation.language_code == language_code)
        )
        if not company_name:
            company_name = session.scalar(
                select(CompanyTranslation.name)
                .where(CompanyTranslation.company_id == company_id)
                .limit(1)
            )
        if company_name:
            results.append(
                CompanyItemResponse(
                    company_name=company_name
                )
            )

    return CompanyItemListResponse(
        data=results
    )


def add_tags_to_company(
    company_name: str,
    tags: List[TagName],
    language_code: str,
    session: Session
) -> CompanyResponse:
    """
    회사 태그 정보 추가
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    """
    company_translation = session.scalar(
        select(CompanyTranslation)
        .where(CompanyTranslation.name == company_name)
    )
    if not company_translation:
        raise NotFoundEx(code="ERR40401")
    company_id = company_translation.company_id

    for tag in tags:
        base_name = tag.tag_name.get("ko") or next(iter(tag.tag_name.values()))
        try:
            tag_id = int("".join(filter(str.isdigit, base_name)))
        except:
            raise BadRequestEx(code="ERR40001")

        tag_group = session.get(TagGroup, tag_id)
        if not tag_group:
            tag_group = TagGroup(id=tag_id)
            session.add(tag_group)
            session.flush()

        for lang, name in tag.tag_name.items():
            exists = session.scalar(
                select(TagGroupTranslation)
                .where(TagGroupTranslation.tag_group_id == tag_id)
                .where(TagGroupTranslation.language_code == lang)
            )
            if not exists:
                session.add(TagGroupTranslation(
                    tag_group_id=tag_id,
                    language_code=lang,
                    name=name
                ))

        existing_link = session.scalar(
            select(CompanyTag)
            .where(CompanyTag.company_id == company_id)
            .where(CompanyTag.tag_group_id == tag_id)
        )
        if not existing_link:
            session.add(CompanyTag(company_id=company_id, tag_group_id=tag_id))

    session.commit()

    name = session.scalar(
        select(CompanyTranslation.name)
        .where(CompanyTranslation.company_id == company_id)
        .where(CompanyTranslation.language_code == language_code)
    ) or session.scalar(
        select(CompanyTranslation.name)
        .where(CompanyTranslation.company_id == company_id)
        .limit(1)
    )

    tag_names = session.scalars(
        select(TagGroupTranslation.name)
        .join(CompanyTag, TagGroupTranslation.tag_group_id == CompanyTag.tag_group_id)
        .where(CompanyTag.company_id == company_id)
        .where(TagGroupTranslation.language_code == language_code)
    ).all()

    return CompanyResponse(
        company_name=name,
        tags=sorted(tag_names, key=lambda x: int("".join(filter(str.isdigit, x))))
    )


def delete_company_tag(
    company_name: str,
    tag_name: str,
    language_code: str,
    session: Session
) -> CompanyResponse:
    """
    회사 태그 정보 삭제
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    """
    company_translation = session.scalar(
        select(CompanyTranslation)
        .where(CompanyTranslation.name == company_name)
    )
    if not company_translation:
        raise NotFoundEx(code="ERR40401")
    company_id = company_translation.company_id

    tag_group_id = session.scalar(
        select(TagGroupTranslation.tag_group_id)
        .where(TagGroupTranslation.name == tag_name)
    )
    if not tag_group_id:
        raise NotFoundEx(code="ERR40401")

    session.execute(
        delete(CompanyTag)
        .where(CompanyTag.company_id == company_id)
        .where(CompanyTag.tag_group_id == tag_group_id)
    )
    session.commit()

    name = session.scalar(
        select(CompanyTranslation.name)
        .where(CompanyTranslation.company_id == company_id)
        .where(CompanyTranslation.language_code == language_code)
    ) or session.scalar(
        select(CompanyTranslation.name)
        .where(CompanyTranslation.company_id == company_id)
        .limit(1)
    )

    tag_names = session.scalars(
        select(TagGroupTranslation.name)
        .join(CompanyTag, TagGroupTranslation.tag_group_id == CompanyTag.tag_group_id)
        .where(CompanyTag.company_id == company_id)
        .where(TagGroupTranslation.language_code == language_code)
    ).all()

    return CompanyResponse(
        company_name=name,
        tags=sorted(tag_names, key=lambda x: int("".join(filter(str.isdigit, x))))
    )
