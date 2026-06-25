import pytest
from dotenv import load_dotenv
from clients.store_client import StoreClient
from clients.admin_client import AdminClient

# 테스트 시작 전 .env 로드
load_dotenv()

@pytest.fixture(scope="session")
def store_client():
    """모든 테스트에서 공용으로 사용할 StoreClient 인스턴스"""
    client = StoreClient()
    return client
@pytest.fixture(scope="session")
def admin_client():
    return AdminClient()