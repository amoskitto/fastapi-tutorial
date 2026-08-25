from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res =authorized_client.get("/posts/")
    
    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate, res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
    
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/888888")
    
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = res.json()
    assert post["id"] == test_posts[0].id
    assert post["title"] == test_posts[0].title
    assert post["content"] == test_posts[0].content
    
@pytest.mark.parametrize("title, content, published", [
    ("Awesome New Post", "This is the content of the awesome post", True),
    ("Second Post", "This is the content of the second post", False),
    ("Third Post", "This is the content of the third post", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={
        "title": title,
        "content": content,
        "published": published
    })
    
 
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title        
    assert created_post.content == content    
    assert created_post.published == published 
    assert created_post.owner_id == test_user["id"]
    
    
def test_create_post_default_publisehed_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={
        "title": "arbituary title",
        "content": "aadjfjfj",
    })
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbituary title"      
    assert created_post.content == "aadjfjfj"           
    assert created_post.published == True               
    assert created_post.owner_id == test_user["id"]
    
    
def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")  # ✅ Fixed
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")  # ✅ Fixed
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/800000")  # ✅ Fixed (no f-string needed)
    assert res.status_code == 404