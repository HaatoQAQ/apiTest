import json

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# 1. GET 请求
def test_get():
    r = requests.get(f"{BASE_URL}/port/1")
    print("状态码：", r.status_code)
    print("响应JSON：", r.json())
    print("响应头：", r.headers["Content-Type"])

# 2. GET带参数
def test_get_with_params():
    r = requests.get(f"{BASE_URL}/posts", params={"userId": 1})
    print("数量：", len(r.json()))

# 3. POST 请求
def test_post():
    data = {"title": "foo", "boby": "bar", "userId": "1"}
    r = requests.post(f"{BASE_URL}/posts", json=data)
    print("状态码：", r.status_code)
    print("返回：", r.json())

# 4. PUT 请求
def test_put():
    data = {"id": "1", "title": "updated", "body": "bar", "userId": 1}
    r = requests.put(f"{BASE_URL}/posts/1", json=data)
    print("状态码：", r.status_code)
    print("返回：", r.json())

# 5. DELETE 请求
def test_delete():
    r = requests.delete(f"{BASE_URL}/posts/1")
    print("状态码：", r.status_code)

if __name__ == "__main__":
    test_get()
    test_get_with_params()
    test_post()
    test_put()
    test_delete()