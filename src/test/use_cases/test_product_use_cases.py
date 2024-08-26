import pytest
from fastapi.exceptions import HTTPException
from db.models import Product as ProductModel
from schemas.product import Product, ProductOutput
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

def test_delete_product(db_session):
    category = CategoryModel(name='Roupa', slug='roupa')
    db_session.add(category)
    db_session.commit()
    
    product_on_db = ProductModel(name= 'Camisa nike', 
                           slug= 'camisa-nike',
                           price=100.99,
                           stock=20,
                           category_id=category.id)
    
    db_session.add(product_on_db)
    db_session.commit()
    
    uc = ProductUseCases(db_session=db_session)
    uc.delete_product(id=product_on_db.id)
    
    products_on_db = db_session.query(ProductModel).all()
    
    assert len(products_on_db) == 0 

def test_delete_product_non_exist(db_session):
    uc = ProductUseCases(db_session=db_session)
    
    with pytest.raises(HTTPException):
        uc.delete_product(id=999)

def test_list_products(db_session):
    category = CategoryModel(name='Roupa', slug='roupa')
    db_session.add(category)
    db_session.commit()
    
    products = [ProductModel(name= 'Camisa Nike', slug= 'camisa-nike', price=100.99, stock=20, category_id=category.id),
                ProductModel(name= 'Camisa Adidas', slug= 'camisa-adidas', price=100.99, stock=20, category_id=category.id),
                ProductModel(name= 'Camisa Hurley', slug= 'camisa-hurley', price=100.99, stock=20, category_id=category.id),
                ProductModel(name= 'Camisa Dc', slug= 'camisa-dc', price=100.99, stock=20, category_id=category.id),
    ]
       
    for product in products:
        db_session.add(product)
    db_session.commit()
    
    for product in products:
        db_session.refresh(product)
    
    
    uc = ProductUseCases(db_session=db_session)
    
    list_products = uc.list_products()
    for product in products:
        db_session.refresh(product)
    
    assert len(products) == 4
    assert type(list_products[0]) == ProductOutput
    assert list_products[0].name == products[0].name
    assert list_products[0].slug == products[0].slug
    assert list_products[0].price == products[0].price
    assert list_products[0].stock == products[0].stock
    assert list_products[0].category.name == products[0].category.name
    
    for product in products:
        db_session.delete(product)
    db_session.commit()
    
    db_session.delete(category)
    db_session.commit()