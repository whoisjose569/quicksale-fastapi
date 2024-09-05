import pytest
from passlib.context import CryptContext
from fastapi.testclient import TestClient
from fastapi import status
from schemas.user import User
from db.models import User as UserModel
from main import app

client = TestClient(app)
crypt_context = CryptContext(schemes=['sha256_crypt'], deprecated="auto")

def test_register_user_route(db_session):
    body = {
        'username': 'pedro',
        'password': 'pass#'
    }
    
    response = client.post('/user/register', json=body)
    
    assert response.status_code == status.HTTP_201_CREATED
    user_on_db = db_session.query(UserModel).first()
    assert user_on_db is not None
    
    db_session.delete(user_on_db)
    db_session.commit()

def test_register_user_route_user_already_exists(db_session):
    user = UserModel(username='jose', password=crypt_context.hash('pass#'))
    db_session.add(user)
    db_session.commit()
    
    body = {
        'username': user.username,
        'password': 'pass#'
    }
    
    response = client.post('/user/register', json=body)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    db_session.delete(user)
    db_session.commit()
    