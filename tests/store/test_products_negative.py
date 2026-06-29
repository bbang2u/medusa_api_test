import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator, FormatChecker

ERROR_SCHEMA_PATH = Path(__file__).parents[2] / "schemas" / "error_response.schema.json"


@pytest.fixture(scope="module")
def error_schema():
    return json.loads(ERROR_SCHEMA_PATH.read_text(encoding="utf-8"))


@pytest.mark.negative
def test_get_nonexistent_product_returns_404(store_client, error_schema):
    """
    [왜] 없는 리소스 요청 시 시스템이 404로 명확히 거부하고,
         에러 응답도 일관된 계약({type, message})을 지키는지 검증.
         클라이언트는 error.message를 노출하고 error.type으로 분기하므로
         에러 응답의 계약 준수가 정상 응답만큼 중요하다.
    [기댓값] 404 + type='not_found' + 에러 스키마 일치
    """
    response = store_client.get_product("prod_INVALIDXXXXXXXXXXXXXXXXXX")

    # 1) 상태코드
    assert response.status_code == 404, f"기대 404, 실제 {response.status_code}"

    # 2) 에러 응답 구조 계약
    body = response.json()
    errors = sorted(
        Draft202012Validator(error_schema, format_checker=FormatChecker()).iter_errors(body),
        key=lambda e: list(e.path),
    )
    assert not errors, "에러 응답 계약 위반:\n" + "\n".join(
        f"  - {list(e.path)}: {e.message}" for e in errors
    )

    # 3) 의미 있는 값 검증 (구조뿐 아니라 값까지)
    assert body["type"] == "not_found", f"기대 type='not_found', 실제 '{body['type']}'"