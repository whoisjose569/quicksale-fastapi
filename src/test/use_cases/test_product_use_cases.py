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
    
    db_session.delete(product_on_db)
    db_session.commit()

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

def test_update_product(db_session):
    category = CategoryModel(name='Roupa', slug='roupa')
    db_session.add(category)
    db_session.commit()
    
    product_on_db = ProductModel(name= 'Camisa Adidas', 
                           slug= 'camisa-adidas',
                           price=100.99,
                           stock=20,
                           category_id=category.id)
    
    db_session.add(product_on_db)
    db_session.commit()

    uc = ProductUseCases(db_session=db_session)
    new_product = Product(
        name= 'Camisa Nike',
        slug= 'camisa-nike',
        price = 22.99,
        stock= 22
    )
    uc.update_product(id=product_on_db.id, product=new_product)
    
    product_updated_on_db = db_session.query(ProductModel).filter_by(id=product_on_db.id).first()
    
    assert product_updated_on_db is not None
    assert product_updated_on_db.name == new_product.name
    assert product_updated_on_db.slug == new_product.slug
    assert product_updated_on_db.price == new_product.price
    assert product_updated_on_db.stock == new_product.stock
    
    db_session.refresh(product_updated_on_db)
    db_session.delete(product_updated_on_db)
    db_session.delete(category)
    db_session.commit()

