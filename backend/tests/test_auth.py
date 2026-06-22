import pytest

def test_register(client):
    response = client.post(
        "/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "註冊成功！歡迎加入，請前往登入。"

def test_login(client):
    # 先註冊
    client.post(
        "/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    
    # 再登入
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client):
    # 先註冊
    client.post(
        "/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    
    # 登入錯誤密碼
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "帳號或密碼錯誤，請再試一次。"

def test_read_users_me(client):
    # 先註冊並登入
    client.post(
        "/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    login_response = client.post(
        "/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    
    # 取得個人資訊
    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
