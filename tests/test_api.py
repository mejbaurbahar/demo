import pytest
import requests

@pytest.mark.api
def test_get_user_api_placeholder():
    """Valid GET request"""
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "Bret"

@pytest.mark.api
def test_get_non_existent_user():
    """Negative test: Non-existent user (404)"""
    response = requests.get("https://jsonplaceholder.typicode.com/users/9999")
    assert response.status_code == 404

@pytest.mark.api
def test_create_post_api():
    """Valid POST request"""
    payload = {"title": "foo", "body": "bar", "userId": 1}
    response = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload)
    assert response.status_code == 201
    assert response.json()["title"] == "foo"

@pytest.mark.api
def test_create_post_empty_data():
    """Edge case: Empty payload"""
    response = requests.post("https://jsonplaceholder.typicode.com/posts", json={})
    # JSONPlaceholder allows empty posts, but in real scenarios might be 400
    assert response.status_code == 201 

@pytest.mark.api
def test_api_latency():
    """Performance/Edge case: Response time check"""
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    assert response.elapsed.total_seconds() < 2.0
