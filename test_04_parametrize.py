import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

# 1. 基础参数化
@pytest.mark.parametrize("post_id", [1,2,3,4,5])
def test_get_post_param(post_id):
    r = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert r.status_code == 200
    assert r.json()["id"] == post_id

# 2. 多参数
@pytest.mark.parametrize("post_id, expected_user", [
    (1,1),
    (2,1),
    (3,1),
    (4,1),
    (5,1)
])
def test_post_user(post_id,expected_user):
    r = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert r.json()["userId"] == expected_user

# 3. 带预期结果的参数化
@pytest.mark.parametrize("post_id, expected_code",[
    (1,200),
    (2,200),
    (99999,404)
])
def test_status_code(post_id, expected_code):
    r = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert r.status_code == expected_code

# 4. 断言分装
def assert_status(resp ,expected=200):
    # 断言状态码
    assert resp.status_code == expected, \
        f"状态码错误: 预期状态码为 {expected}, 实际为 {resp.status_code}"

def assert_json_key(resp, key):
    # 断言响应中是否包含某个字段
    assert key in resp.json(), f"响应数据中不包含字段 {key}"

def assert_json_value(resp, key, expected):
    value = resp.json().get(key)
    assert value == expected, f"字段 {key} 错误: 预期 {expected}, 实际 {value}"

def test_with_assert_helpers():
    r = requests.get(f"{BASE_URL}/posts/1")
    assert_status(r,200)
    assert_json_key(r,"title")
    assert_json_key(r, "body")
    assert_json_value(r, "id", 1)

# 6. 断言分装+参数化结合
@pytest.mark.parametrize("post_id", [1,2,3,4])
def test_combined(post_id):
    r = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert_status(r,200)
    assert_json_key(r,"title")
    assert_json_value(r,"id",post_id)

# 7. 参数化数据从列表来
login_cases = [
    ("admin", "123456", 200, "登录成功"),
    ("admin", "wrong", 401, "密码错误"),
    ("wrong", "123456", 401, "用户不存在"),
    ("", "", 400, "参数为空"),
]

@pytest.mark.parametrize("username, password, expected_code, desc",login_cases)
def test_login(username, password, expected_code, desc):
    r = requests.post("login_url",json={"username": username, "password": password})
