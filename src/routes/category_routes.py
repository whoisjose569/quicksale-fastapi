from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, status
from schemas.category import Category
from routes.deps import get_db_session
from use_cases.category import CategoryUseCases

router = APIRouter(prefix='/category', tags=['Category'])

@router.post('/add')
def add_category(category: Category, db_session: Session = Depends(get_db_session)):
    uc = CategoryUseCases(db_session=db_session)
    uc.add_category(category=category)
    return Response(status_code=status.HTTP_201_CREATED)