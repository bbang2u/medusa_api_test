# clients/admin_client.py
import os
from .base_client import BaseClient


class AdminClient(BaseClient):
    def __init__(self, base_url=None):
        super().__init__(base_url)
        self._authenticate()

    def _authenticate(self):
        email = os.getenv("MEDUSA_ADMIN_EMAIL")
        password = os.getenv("MEDUSA_ADMIN_PASSWORD")

        if not email or not password:
            raise EnvironmentError("MEDUSA_ADMIN_EMAIL / MEDUSA_ADMIN_PASSWORD가 .env에 없습니다.")

        resp = self._request(
            "POST",
            "/auth/user/emailpass",
            json={"email": email, "password": password},
        )

        if resp.status_code != 200:
            raise RuntimeError(f"Admin 로그인 실패: {resp.status_code} {resp.text}")

        token = resp.json()["token"]
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    # admin API 메서드들
    def get_users(self, query_params=None):
        """관리자 사용자 목록 조회"""
        return self._request("GET", "/admin/users", params=query_params)