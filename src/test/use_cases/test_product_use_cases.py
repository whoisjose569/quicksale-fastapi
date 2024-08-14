import pytest
from fastapi.exceptions import HTTPException
from db.models import Product as ProductModel
from schemas.product import Product
from use_cases.category import CategoryUseCases
from use_cases.product import ProductUseCases
from db.models import Category as CategoryModel
from schemas.category import Category

def test_add_product_uc(db_session):
    uc = ProductUseCases(db_session)
    uc2 = CategoryUseCases(db_session)
    
    category = Category(
        name='Malha',
        slug='malha'
    )
    
    uc2.add_category(category=category)
    
    product = Product(
        name= 'Camisa Nike',
        slug= 'camisa-nike',
        price = 22.99,
        stock= 22
    )
    categories_on_db = db_session.query(CategoryModel).filter_by(slug=category.slug).first()

    
    uc.add_product(product=product, category_slug=categories_on_db.slug)
    
    product_on_db = db_session.query(ProductModel).first()
    
    assert product_on_db is not None
    assert product_on_db.name == product.name
    assert product_on_db.slug == product.slug
    assert product_on_db.price == product.price
    assert product_on_db.stock == product.stock

def test_add_product_uc_invalid_category(db_session):
    uc = ProductUseCases(db_session)
    
    product = Product(
        name= 'Camisa Nike',
        slug= 'camisa-nike',
        price = 22.99,
        stock= 22
    )
    
    with pytest.raises(HTTPException):
        uc.add_product(product=product, category_slug='invalid')