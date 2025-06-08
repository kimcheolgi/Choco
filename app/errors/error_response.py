from typing import Dict
from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    msg: str
    data: dict = None
    code: str
    status_code: str


error_response_map: Dict[str, ErrorResponseModel] = {
    "ERR50001": ErrorResponseModel(msg="Internal Server Error", code="ERR50001", status_code="500"),
    "ERR40001": ErrorResponseModel(msg="Bad Request Error", code="ERR40002", status_code="400"),
    "ERR40101": ErrorResponseModel(msg="Unauthorized Error", code="ERR40101", status_code="401"),
    "ERR40301": ErrorResponseModel(msg="Forbidden Error", code="ERR40301", status_code="403"),
    "ERR40401": ErrorResponseModel(msg="Data Not Found Error", code="ERR40401", status_code="404"),
    "ERR40901": ErrorResponseModel(msg="Duplicate Data Error", code="ERR40901", status_code="409"),
    "ERR40902": ErrorResponseModel(msg="Status Condition Not Met Error", code="ERR40902", status_code="409"),
}
