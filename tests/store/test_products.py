def test_get_products_status_code(store_client):
    """상품 목록을 조회했을 때 200 OK가 오는지 확인"""
    response = store_client.get_products()
    
    # 여기서 실패한다면 1) 서버가 꺼져있거나, 2) API Key가 틀렸거나, 3) URL이 잘못된 것
    assert response.status_code == 200, f"예상치 못한 상태코드: {response.status_code}"
    print("\n[성공] API 서버와 인증 통신이 정상입니다!")