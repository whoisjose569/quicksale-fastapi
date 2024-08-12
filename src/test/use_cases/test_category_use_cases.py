import pytest
from use_cases.category import CategoryUseCases
from db.models import Category as CategoryModel
from schemas.category import Category, CategoryOutput
from fastapi.exceptions import HTTPException

def test_add_category_uc(db_session):
    uc = CategoryUseCases(db_session)
    
    category = Category(
        name='Roupa',
        slug='roupa'
    )
    
    uc.add_category(category=category)
    
    categories_on_db = db_session.query(CategoryModel).all()
    assert len(categories_on_db) == 1
    assert categories_on_db[0].name == 'Roupa'
    assert categories_on_db[0].slug == 'roupa'
    
def test_list_category_uc(db_session):
    uc = CategoryUseCases(db_session=db_session)
    categories = [
        CategoryModel(name='Roupa', slug='roupa'),
        CategoryModel(name='Carro', slug='carro'),
        CategoryModel(name='Celular', slug='celular'),
        CategoryModel(name='Decoracao', slug='decoracao')
    ]
    
    for category in categories:
        db_session.add(category)
    db_session.commit()
    
    categories = uc.list_categories()
    categories_on_db = db_session.query(CategoryModel).all()
    
    
    assert len(categories) == 4
    assert type(categories[0]) == CategoryOutput
    assert categories[0].id == categories_on_db[0].id
    assert categories[0].name == categories_on_db[0].name
    assert categories[0].slug == categories_on_db[0].slug
    

def test_delete_category_uc(db_session):
    category_model = CategoryModel(name='Celular', slug='celular')
    db_session.add(category_model)
    db_session.commit()
    
    uc = CategoryUseCases(db_session=db_session)
    uc.delete_category(id=category_model.id)
    
    category_model = db_session.query(CategoryModel).filter_by(id=category_model.id).first()
    assert category_model is None

def test_delete_category_non_exist(db_session):

    uc = CategoryUseCases(db_session=db_session)
    with pytest.raises(HTTPException):
        uc.delete_category(id=999)

