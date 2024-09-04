import pytest
from schemas.user import User

def test_user_schema():
    user = User(username='Jose', password='pass')
    
    assert user.dict() == {
        'username': 'Jose',
        'password': 'pass'
    }

def test_user_schema_invalid_username():
    with pytest.raises(ValueError):
        user = User(username='João#', password='pass')
    