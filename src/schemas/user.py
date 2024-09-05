import re
from pydantic import field_validator
from datetime import datetime
from schemas.base import CustomBaseModel

class User(CustomBaseModel):
    username: str
    password: str
    
    @field_validator('username', mode='before')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[A-Z]|[0-9]|-|_|@)+$', value):
            raise ValueError('Invalid username')
        return value

class TokenData(CustomBaseModel):
    access_token: str
    expires_at: datetime