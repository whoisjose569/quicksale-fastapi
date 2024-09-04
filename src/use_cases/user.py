from sqlalchemy.orm import Session
from passlib.context import CryptContext
from schemas.user import User
from db.models import User as UserModel
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.exc import IntegrityError

crypt_context = CryptContext(schemes=['sha256_crypt'], deprecated="auto")

class UserUseCases:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    def register_user(self, user: User):
        user_on_db = UserModel(
            username=user.username,
            password=crypt_context.hash(user.password)
        )
        
        self.db_session.add(user_on_db)
        try:
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exists')