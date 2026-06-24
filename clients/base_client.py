import requests
import logging
import os

# 로깅 설정: 테스트 실행 시 터미널에 어떤 요청이 오가는지 보여줍니다.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseClient:
    def __init__(self, base_url=None):
        # 환경변수에서 URL을 가져오거나 기본값 사용
        self.base_url = base_url or os.getenv("MEDUSA_BASE_URL", "http://localhost:9000")
        self.session = requests.Session()
        
    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Sending {method} request to {url}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            # 상태 코드가 400 이상일 경우 경고 로그 출력
            if response.status_code >= 400:
                logger.error(f"Error {response.status_code}: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise