import pytest

from fastapi import Depends, FastAPI, Security
from fastapi.security import OAuth2, OAuth2PasswordRequestFormStrict
from fastapi.testclient import TestClient
from pydantic import BaseModel

from main import app


client = TestClient(app)

#Tests before auth
def new():
    req = {
        "body": "It works!",
    }
    #add 
    response = client.post("/post/new", json=req)
    assert response.status_code == 201

    id = response.json()['id']

    #get
    response_sec = client.get("/post/" + str(id))
    assert response_sec.status_code == 200
    assert response_sec.json()['counter'] == 1

    #get2
    response_sec = client.get("/post/" + str(id))
    assert response_sec.status_code == 200
    assert response_sec.json()['counter'] == 2
    return id

def test_get_post():
    response = client.get("/post/5")
    assert response.status_code == 404
    response = client.get("/post/7")
    response_sec = client.get("/post/7")
    assert response_sec.status_code == 200
    assert response.json()['counter'] + 1 == response_sec.json()['counter']

def test_add_new_post():
    req = {
        "body": "It works!",
    }
    response = client.post("/post/new", json=req)
    assert response.status_code == 201
    assert response.json()['body'] == "It works!"
    str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut ac sollicitudin augue. Vivamus ac tempus libero. Cras vitae massa faucibus odio tempor ullamcorper. Ala"
    req = {
        "body":  str
    }
    response = client.post("/post/new", json=req)
    assert response.status_code == 201
    assert response.json()['body'] == str[:160]

def test_post_destroy():
    req = {
        "body": "It works!",
    }
    response = client.post("/post/new", json=req)
    assert response.status_code == 201
    id = response.json()['id']
    response = client.delete("post/" + str(id))
    assert response.status_code == 204
    response = client.delete("post/" + str(id))
    assert response.status_code == 404


#post not found
def test_post_not_found():
    req = {
        "body": "It works!",
    }
    response = client.put("/post/1", json=req)
    assert response.status_code == 404


def test_post_update_new_text():
    id = new()
    #update new 
    req = {
        "body": "New text!",
    }
    response = client.put("/post/" + str(id), json=req)
    assert response.status_code == 202
    #check if counter is again set to 0
    response = client.get("/post/" + str(id))
    assert response.status_code == 200
    assert response.json()['counter'] == 1 


def test_post_update_same_text():
    id = new()
    #update new
    req = {
        "body": "It works!",
    }
    response = client.put("/post/" + str(id), json=req)
    assert response.status_code == 400
    response = client.get("/post/" + str(id))
    assert response.status_code == 200
    assert response.json()['counter'] == 3 
