import pytest
from app import models


@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()



def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    
    assert res.status_code == 201

def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    
    assert res.status_code == 409
    
    
def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201  # Vote removed

def test_delete_vote_non_exist(authorized_client):
    res = authorized_client.post("/vote/", json={"post_id": 999999, "dir": 0})
    assert res.status_code == 404  # Post not found

def test_vote_unauthorized_user(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 401  # Vote not found
    
#assignment to implement so a user cant vote on his or her own post and also write test for that as well 