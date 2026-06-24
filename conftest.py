import pytest
from dotenv import load_dotenv
from clients.store_client import StoreClient

# 테스트 시작 전 .env 로드
load_dotenv()

@pytest.fixture(scope="session")
def store_client():
    """모든 테스트에서 공용으로 사용할 StoreClient 인스턴스"""
    client = StoreClient()
    return client