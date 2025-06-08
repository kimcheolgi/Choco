from app.errors.error_response import error_response_map


class StatusCode:
    HTTP_204 = 204
    HTTP_500 = 500
    HTTP_501 = 501
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405
    HTTP_202 = 202
    HTTP_409 = 409


class APIException(Exception):
    status_code: int
    msg: str
    code: str
    ex: Exception
    data: dict

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_500,
        msg: str = error_response_map.get("ERR50001").msg,
        code: str = "ERR50001",
        ex: Exception = None,
        data: dict = None,
    ):
        self.status_code = status_code
        self.msg = msg
        self.code = code
        self.ex = ex
        self.data = data
        super().__init__(ex)


class NotFoundEx(APIException):
    def __init__(self, ex: Exception = None, code: str = None, data: dict = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            msg=error_response_map.get("ERR40401").msg if code is None else error_response_map.get(code).msg,
            code="ERR40401" if code is None else code,
            ex=ex,
            data=data,
        )


class SqlFailureEx(APIException):
    def __init__(self, ex: Exception = None, code: str = None, data: dict = None):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            msg=error_response_map.get("ERR50002").msg if code is None else error_response_map.get(code).msg,
            code="ERR50002" if code is None else code,
            ex=ex,
            data=data,
        )


class InternalServerEx(APIException):
    def __init__(self, ex: Exception = None, code: str = None, data: dict = None):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            msg=error_response_map.get("ERR50001").msg if code is None else error_response_map.get(code).msg,
            code="ERR50001" if code is None else code,
            ex=ex,
            data=data,
        )


class UnauthorizedEx(APIException):
    def __init__(self, ex: Exception = None, data: dict = None, code: str = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=error_response_map.get("ERR40101").msg if code is None else error_response_map.get(code).msg,
            code="ERR40101" if code is None else code,
            ex=ex,
            data=data,
        )


class JWTDecodeEx(APIException):
    def __init__(self, ex: Exception = None, data: dict = None, code: str = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=error_response_map.get("ERR40105").msg if code is None else error_response_map.get(code).msg,
            code="ERR40105" if code is None else code,
            ex=ex,
            data=data,
        )


class DuplicateDataEx(APIException):
    def __init__(self, ex: Exception = None, code: str = None, data: dict = None):
        super().__init__(
            status_code=StatusCode.HTTP_409,
            msg=error_response_map.get("ERR40901").msg if code is None else error_response_map.get(code).msg,
            code="ERR40901" if code is None else code,
            ex=ex,
            data=data,
        )


class ExceededMaximumEx(APIException):
    def __init__(self, ex: Exception = None, code: str = None, data: dict = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=error_response_map.get("ERR40001").msg if code is None else error_response_map.get(code).msg,
            code="ERR40001" if code is None else code,
            ex=ex,
            data=data,
        )


class FileSizeEx(APIException):
    def __init__(self, ex: Exception = None, code: str = None, data: dict = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=error_response_map.get("ERR40003").msg if code is None else error_response_map.get(code).msg,
            code="ERR40003" if code is None else code,
            ex=ex,
            data=data,
        )


class FileContentTypeEx(APIException):
    def __init__(self, ex: Exception = None, code: str = None, data: dict = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=error_response_map.get("ERR40005").msg if code is None else error_response_map.get(code).msg,
            code="ERR40005" if code is None else code,
            ex=ex,
            data=data,
        )


class BadRequestEx(APIException):
    def __init__(self, ex: Exception = None, code: str = None, data: dict = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=error_response_map.get("ERR40002").msg if code is None else error_response_map.get(code).msg,
            code="ERR40002" if code is None else code,
            ex=ex,
            data=data,
        )


class StatusConditionNotMetEx(APIException):
    def __init__(self, ex: Exception = None, code: str = None, data: dict = None):
        super().__init__(
            status_code=StatusCode.HTTP_409,
            msg=error_response_map.get("ERR40902").msg if code is None else error_response_map.get(code).msg,
            code="ERR40902" if code is None else code,
            ex=ex,
            data=data,
        )


class ExpiredSignatureEx(APIException):
    def __init__(self, ex: Exception = None, code: str = None, data: dict = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=error_response_map.get("ERR40106").msg if code is None else error_response_map.get(code).msg,
            code="ERR40106" if code is None else code,
            ex=ex,
            data=data,
        )


class ForbiddenEx(APIException):
    def __init__(self, ex: Exception = None, code: str = None, data: dict = None):
        super().__init__(
            status_code=StatusCode.HTTP_403,
            msg=error_response_map.get("ERR40301").msg if code is None else error_response_map.get(code).msg,
            code="ERR40301" if code is None else code,
            ex=ex,
            data=data,
        )