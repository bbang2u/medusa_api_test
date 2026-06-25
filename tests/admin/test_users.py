# tests/admin/test_users.py
def test_admin_users_authenticated_access(admin_client):
    """
    인증 체인 검증: 로그인→JWT 발급→Bearer 주입→admin 접근이
    전 구간 정상 동작하는지 확인.
    스모크지만 '200'만 보지 않고 응답 구조(users 배열)까지 확인한다.
    """
    response = admin_client.get_users()

    assert response.status_code == 200, f"예상치 못한 상태코드: {response.status_code}"

    body = response.json()
    assert "users" in body, "응답에 users 키가 없음"
    assert isinstance(body["users"], list), "users가 배열이 아님"