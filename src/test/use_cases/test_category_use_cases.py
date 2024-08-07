from use_cases.category import CategoryUseCases
from db.models import Category as CategoryModel
from schemas.category import Category, CategoryOutput

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
    
    
