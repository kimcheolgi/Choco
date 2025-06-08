import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.middlewares.access_validator import access_control
from app.middlewares.trusted_hosts import TrustedHostMiddleware
from app.routes.v1 import company
from app.database.conn_sqlalchemy import db, Base
from app.common.config import conf
from dataclasses import asdict

description = """
Choco API Swagger. 🚀
"""


def create_app():
    """
    앱 함수 실행
    :return:
    """
    app = FastAPI(
        title="Choco API v1.0",
        description=description,
        version="0.0.1",
    )
    c = conf()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)
    # 데이터 베이스 이니셜라이즈
    Base.metadata.create_all(db.engine)

    # 미들웨어 정의
    app.add_middleware(middleware_class=BaseHTTPMiddleware,
                       dispatch=access_control)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=conf().TRUSTED_HOSTS,
        except_path=["/health"]
    )

    # 라우터 정의
    app.include_router(company.router, tags=['회사'])
    
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
