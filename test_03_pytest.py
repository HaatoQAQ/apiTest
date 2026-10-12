import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# 1. 基础用例
def test_get_post():
    r = requests.get(f"{BASE_URL}/posts/1")
    assert r.status_code == 200
    data = r.json()
    print("data = ", data)
    assert data["id"] == 1
    assert "title" in data

# 2. 断言多个字段
def test_post_fields():
    r = requests.get(f"{BASE_URL}/posts/1")
    data = r.json()
    assert data["userId"] == 1
    assert isinstance(data["title"], str)
    assert len(data["title"]) > 0

# 3. 异常场景
def test_not_found():
    r = requests.get(f"{BASE_URL}/posts/99999")
    assert r.status_code == 404

# 4. fixture 前置/后置
@pytest.fixture(scope="session")
def session():
    print("\n[前置] 创建 session")
    s = requests.session()
    s.headers.update({"User-Agent": "pytest"})
    yield s
    print("\n[后置] 关闭 Session")
    s.close()

def test_with_fixture(session):
    r = session.get(f"{BASE_URL}/posts/1")
    assert r.status_code == 200

# 5. 多个用例共用一个fixture
def test_post1(session):
    r = session.get(f"{BASE_URL}/posts/1")
    assert r.status_code == 200

def test_post2(session):
    r = requests.get(f"{BASE_URL}/posts/1")
    assert r.status_code == 200

# 6. assert 失败信息
def test_assert_with_message():
    r = requests.get(f"{BASE_URL}/posts/1")
    assert r.status_code == 100, f"状态码错误:预期100,实际{r.status_code}"
    assert "title1" in r.json(), f"相应缺少title1字段: {r.json()}"