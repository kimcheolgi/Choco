from typing import Dict

from app.errors.error_response import error_response_map


def generate_error_responses(*error_codes: str) -> Dict[int, dict]:
    """
    주어진 에러 코드들에 대해 FastAPI의 `responses` 형식으로 반환
    :param error_codes: 사용할 에러 코드들
    :return: dict 형식의 responses
    """
    # status_code를 기준으로 ErrorResponseModel 리스트를 매핑
    responses: Dict[int, dict] = {}

    for code in error_codes:
        # ErrorResponseModel 가져오기
        error_model = error_response_map.get(code)

        if error_model:
            status_code = error_model.status_code
            # responses의 status_code에 에러 모델 추가
            if status_code not in responses:
                responses[status_code] = {"content": {"application/json": {"examples": {}}}}

            # 각 status_code 아래에 해당 에러 메시지와 코드 추가
            responses[status_code]["content"]["application/json"]["examples"][code] = {
                "summary": error_model.msg,
                "value": {"msg": error_model.msg, "code": error_model.code, "data": error_model.data}
            }

    return responses
