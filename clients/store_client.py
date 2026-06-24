import os
from .base_client import BaseClient

class StoreClient(BaseClient):
    def __init__(self, base_url=None):
        # 1. BaseClient의 __init__을 먼저 호출해서 session을 준비합니다.
        super().__init__(base_url)
        
        # 2. Publishable API Key를 환경변수에서 가져옵니다.
        # 주의: 이 키는 절대 코드에 직접 쓰지 말고, .env 파일이나 OS 환경변수로 관리하세요.
        pub_key = os.getenv("MEDUSA_PUB_KEY")
        
        # 3. 세션 헤더에 기본 키를 박아둡니다.
        # 이렇게 하면 이 클라이언트를 사용하는 모든 요청에 자동으로 이 헤더가 들어갑니다.
        if pub_key:
            self.session.headers.update({"x-publishable-api-key": pub_key})
        else:
            # 안전장치: 키가 없으면 테스트 실행 전 에러를 띄우는 것이 좋습니다.
            raise EnvironmentError("MEDUSA_PUB_KEY가 환경변수에 설정되어 있지 않습니다.")

    # 이제 필요한 API 메서드들을 여기서 정의합니다.
    def get_products(self, query_params=None):
        """상품 목록 조회"""
        return self._request("GET", "/store/products", params=query_params)

    def create_cart(self):
        """장바구니 생성"""
        return self._request("POST", "/store/carts")
    
    def get_cart(self, cart_id):
        """장바구니 상세 조회"""
        return self._request("GET", f"/store/carts/{cart_id}")