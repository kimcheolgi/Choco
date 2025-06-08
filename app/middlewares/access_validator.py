import time
import re
import sys

import sqlalchemy.exc
from aws_xray_sdk.core.async_context import AsyncContext
from opentelemetry.trace import Status, StatusCode

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.common.consts import EXCEPT_PATH_LIST, EXCEPT_PATH_REGEX
from app.errors.exceptions import APIException, SqlFailureEx, UnauthorizedEx

from app.utils.date_utils import D
from app.utils.logger_fastapi import api_logger
from os import environ
from opentelemetry import trace


async def access_control(request: Request, call_next):
    request.state.req_time = D.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    request.state.service = None
    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host if request.client is not None else "localhost"
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    headers = request.headers
    url = request.url.path
    if await url_pattern_check(url, EXCEPT_PATH_REGEX) or url in EXCEPT_PATH_LIST:
        response = await call_next(request)
        if url != "/":
            await api_logger(request=request, response=response)
        return response

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span(f"{request.method} {url}") as span:
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))
        span.set_attribute("environment", environ.get("API_ENV"))
        span.set_attribute("client.ip", ip)
        try:
            response = await call_next(request)
            span.set_attribute("http.status_code", response.status_code)
            span.set_status(Status(StatusCode.OK))
            await api_logger(request=request, response=response)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
    
            # traceback의 최상단 프레임 가져오기
            while exc_traceback.tb_next:
                exc_traceback = exc_traceback.tb_next
            frame = exc_traceback.tb_frame
    
            # frame을 request.state에 저장
            request.state.inspect = frame
            error = await exception_handler(e)
            error_dict = dict(msg=error.msg, data=error.data, code=error.code)
            response = JSONResponse(status_code=error.status_code, content=error_dict)

            span.set_attribute("http.status_code", response.status_code)
            if 400 <= error.status_code < 500:
                span.set_attribute("error.severity", "WARNING")
            else:
                span.set_attribute("error.severity", "ERROR")
                span.set_status(Status(StatusCode.ERROR, description="Server error"))
            span.record_exception(e)

            await api_logger(request=request, error=error)
    return response


async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def exception_handler(error: Exception):
    if isinstance(error, sqlalchemy.exc.OperationalError):
        error = SqlFailureEx(ex=error)
    if not isinstance(error, APIException):
        error = APIException(ex=error)
    return error