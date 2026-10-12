import json
from zoneinfo import reset_tzpath

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# 1. 不用Session，每次请求都是新的连接
def test_no_session():
    r1 = requests.get(f"{BASE_URL}/posts/1")
    r2 = requests.get(f"{BASE_URL}/posts/2")
    print("r1:", r1.status_code)
    print("r2:", r2.status_code)
    print("不用 Session, 两次请求互不关联")

# 2. 用 Session,保持Cookie,复用连接,统一请求头
def test_session():
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0"})

    r1 = s.get(f"{BASE_URL}/posts/1")
    r2 = s.get(f"{BASE_URL}/posts/2")

    print("r1: ", r1.status_code)
    print("r2: ", r2.status_code)
    print("Session 内的 Cookies", s.cookies)
    s.close()

# 3. 模拟登录: 拿到Token,后续请求带上Token
def test_token():
    s = requests.Session()

    # 3.1 登录,拿到Token
    login_resp = s.post(
        "https://httpbin.org/post",
        json={"username": "admin", "password": "123456"}
    )
    print("登录响应:", login_resp.json()["json"])

    # 3.2 假设服务器返回的 token 在json 里
    token = "fake_token_123456"

    # 3.3 后续请求带上token
    headers = {"Authorization": f"Bearer {token}"}
    r = s.get("https://httpbin.org/get", headers=headers)
    print("带 Token 请求的 headers:", r.json()["headers"])

    s.close()

# 4. Session 保持登录态的真实写法
def test_login_keep_session():
    s = requests.Session()

    # 登录
    s.post(
        "https://httpbin.org/post",
        json={"username": "admin", "password": "123456"}
    )

    # 后续请求自动带上登录后的Cookie
    r = s.get("https://httpbin.org/cookies")
    print("当前 Cookies:", r.json())
    s.close()

# 5. 查看cookie是否过期
def test_cookie_expire():
    s = requests.Session()
    r = s.get("http://httpbin.org/cookies/set?sessionId=abc123")

    for cookie in s.cookies:
        print("过期时间:", cookie.expires)
        print("名称:", cookie.name)

if __name__ == "__main__":
    test_no_session()
    print("-" * 40)
    test_session()
    print("-" * 40)
    test_token()
    print("-" * 40)
    test_login_keep_session()
    print("-" * 40)
    test_cookie_expire()