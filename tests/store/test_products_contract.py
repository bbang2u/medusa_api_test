import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_PATH = Path(__file__).parents[2] / "schemas" / "store_product_list.schema.json"


@pytest.fixture(scope="module")
def product_list_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@pytest.mark.contract
def test_store_products_matches_contract(store_client, product_list_schema):
    """
    /store/products 응답이 OpenAPI 명세 기반 계약을 지키는지 검증.
    200만 보지 않고 구조·타입·enum·날짜포맷까지 명세와 일치하는지 본다.
    """
    response = store_client.get_products(query_params={"limit": 50})
    assert response.status_code == 200

    body = response.json()
    validator = Draft202012Validator(product_list_schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(body), key=lambda e: list(e.path))

    assert not errors, "계약 위반:\n" + "\n".join(
        f"  - {list(e.path)}: {e.message}" for e in errors
    )