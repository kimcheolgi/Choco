from sqlalchemy import (
    Column, BigInteger, String, Text, DateTime, ForeignKey
)
from app.database.conn_sqlalchemy import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Company(Base):
    __tablename__ = "company"
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    translations = relationship("CompanyTranslation", back_populates="company")
    tags = relationship("CompanyTag", back_populates="company")


class CompanyTranslation(Base):
    __tablename__ = "company_translation"
    id = Column(BigInteger, primary_key=True)
    company_id = Column(BigInteger, ForeignKey("company.id"), nullable=False)
    language_code = Column(String(10), nullable=False)
    name = Column(Text, nullable=False)

    company = relationship("Company", back_populates="translations")


class TagGroup(Base):
    __tablename__ = "tag_group"
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    translations = relationship("TagGroupTranslation", back_populates="tag_group")
    companies = relationship("CompanyTag", back_populates="tag_group")


class TagGroupTranslation(Base):
    __tablename__ = "tag_group_translation"
    id = Column(BigInteger, primary_key=True)
    tag_group_id = Column(BigInteger, ForeignKey("tag_group.id"), nullable=False)
    language_code = Column(String(10), nullable=False)
    name = Column(Text, nullable=False)

    tag_group = relationship("TagGroup", back_populates="translations")


class CompanyTag(Base):
    __tablename__ = "company_tag"
    id = Column(BigInteger, primary_key=True)
    company_id = Column(BigInteger, ForeignKey("company.id"), nullable=False)
    tag_group_id = Column(BigInteger, ForeignKey("tag_group.id"), nullable=False)

    company = relationship("Company", back_populates="tags")
    tag_group = relationship("TagGroup", back_populates="companies")
