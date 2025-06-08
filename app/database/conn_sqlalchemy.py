from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging
from app.common.consts import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE
from sqlalchemy import text


def _database_exist(engine, schema_name):
    query = f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{schema_name}'"
    with engine.connect() as conn:
        result_proxy = conn.execute(text(query))
        result = result_proxy.scalar()
        return bool(result)


def _drop_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE {schema_name};"))


def _create_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE {schema_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"))


class SQLAlchemy:
    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine = None
        self._session = None
        self._engine_dict = None
        self._session_dict = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):
        """
        DB 초기화 함수
        :param app: FastAPI 인스턴스
        :param kwargs:
        :return:
        """
        is_testing = kwargs.setdefault("TEST_MODE", False)

        database_url = kwargs.get("DB_HOST") # use test case
        if is_testing:
            database_url_dict = {
                "db": f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
            }
        else:
            database_url_dict = {
                "db": f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
            }
        pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
        echo = kwargs.setdefault("DB_ECHO", True)
        self._engine_dict = {
            "db": create_engine(
                database_url_dict['db'],
                echo=echo,
                pool_recycle=pool_recycle,
                pool_pre_ping=True,
            )
        }

        self._session_dict = {
            "db": sessionmaker(autocommit=False, autoflush=False, bind=self._engine_dict['db'])
        }

        @app.on_event("startup")
        def startup():
            self._engine_dict["db"].connect()
            logging.info("DB connected.")

        @app.on_event("shutdown")
        def shutdown():
            self._session_dict['db'].close_all()
            self._engine_dict["db"].dispose()
            logging.info("DB disconnected")

    def get_writer_db(self):
        """
        요청마다 DB 세션 유지 함수
        :return:
        """
        if self._session_dict['db'] is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session_dict['db']()
            yield db_session
        finally:
            db_session.close()
    
    def get_background_writer_db(self):
        """
        백그라운드 작업에서 사용할 새로운 DB 세션 생성 함수
        :return: session
        """
        if self._session_dict['db'] is None:
            raise Exception("must be called 'init_app'")
        db_session = self._session_dict['db']()
        return db_session
    
    @property
    def session_writer(self):
        return self.get_writer_db

    def get_reader_db(self):
        """
        요청마다 DB 세션 유지 함수
        :return:
        """
        if self._session_dict['db'] is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session_dict['db']()
            yield db_session
        finally:
            db_session.close()

    @property
    def session_reader(self):
        return self.get_reader_db

    @property
    def engine(self):
        return self._engine_dict['db']


db = SQLAlchemy()
Base = declarative_base()
