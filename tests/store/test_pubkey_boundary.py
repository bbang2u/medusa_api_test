import os
import json
from pathlib import Path
import pytest
import requests
from jsonschema import Draft202012Validator, FormatChecker

ERROR_SCHEMA_PATH = Path(__file__).parents[2] / "schemas" / "error_response.schema.json"
BASE_URL = os.getenv("MEDUSA_BASE_URL", "http://localhost:9000")


@pytest.fixture(scope="module")
def error_schema():
    return json.loads(ERROR_SCHEMA_PATH.read_text(encoding="utf-8"))


def _assert_error_contract(body, schema):
    """에러 응답이 공용 계약({type, message})을 지키는지 검증 (재사용 헬퍼)"""
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(body),
        key=lambda e: list(e.path),
    )
    assert not errors, "에러 응답 계약 위반:\n" + "\n".join(
        f"  - {list(e.path)}: {e.message}" for e in errors
    )


@pytest.mark.negative
def test_missing_pubkey_is_rejected(error_schema):
    """
    [왜] Store API는 publishable key로 클라이언트를 식별한다.
         키 없는 요청을 시스템이 거부하는지 = 인증 경계의 기본선 검증.
    [기댓값] 400 + type='not_allowed' + message에 'required' (누락임을 명시)
    """
    resp = requests.get(f"{BASE_URL}/store/products", params={"limit": 1})  # 헤더 없음

    assert resp.status_code == 400, f"기대 400, 실제 {resp.status_code}"
    body = resp.json()
    _assert_error_contract(body, error_schema)
    assert body["type"] == "not_allowed"
    assert "required" in body["message"].lower(), \
        f"누락 케이스 메시지에 'required' 없음: {body['message']}"


@pytest.mark.negative
def test_invalid_pubkey_is_rejected(error_schema):
    """
    [왜] 키가 '존재하긴 하나 유효하지 않은' 경우도 거부해야 한다.
         유효하지 않은 인증수단을 조용히 통과시키면(예: 200) 인증 우회 결함.
         누락(required)과 다른 메시지인지까지 봐서 시스템이 두 상황을
         구분 인지하는지 검증한다.
    [기댓값] 400 + type='not_allowed' + message에 'valid' (무효임을 명시)
    """
    resp = requests.get(
        f"{BASE_URL}/store/products",
        params={"limit": 1},
        headers={"x-publishable-api-key": "pk_THIS_IS_WRONG_123"},
    )

    assert resp.status_code == 400, f"기대 400, 실제 {resp.status_code}"
    body = resp.json()
    _assert_error_contract(body, error_schema)
    assert body["type"] == "not_allowed"
    assert "valid" in body["message"].lower(), \
        f"무효 케이스 메시지에 'valid' 없음: {body['message']}"