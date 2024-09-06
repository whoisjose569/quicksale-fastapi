from fastapi.testclient import TestClient
from fastapi import status
from db.models import Product as ProductModel
from main import app
from db.models import Category as CategoryModel

client = TestClient(app)
headers = {"Authorization": "Bearer token"}
client.headers = headers

def test_add_product_route(db_session):
    categories_on_db = db_session.query(CategoryModel).all()
    body= {
        "category_slug": categories_on_db[0].slug,
        "product": {
            "name": "Camisa Nike",
            "slug": "camisa-nike",
            "price": 23.99,
            "stock": 20
        }
    }
    
    response = client.post('/product/add', json=body)
    
    assert response.status_code == status.HTTP_201_CREATED
    
    products_on_db = db_session.query(ProductModel).all()
    
    assert len(products_on_db) == 1
    
    db_session.delete(products_on_db[0])
    db_session.commit()
    
def test_add_product_route_invalid_category_slug(db_session):
    body= {
        "category_slug": "invalid",
        "product": {
            "name": "Camisa Nike",
            "slug": "camisa-nike",
            "price": 23.99,
            "stock": 20
        }
    }
    
    response = client.post('/product/add', json=body)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    products_on_db = db_session.query(ProductModel).all()
    
    assert len(products_on_db) == 0
    
def test_update_product_route(db_session):
    category_model= CategoryModel(name='Roupa', slug='roupa')
    db_session.add(category_model)
    db_session.commit()
    
    new_product = {
        "category_slug": "roupa",
        "product": {
            "name": "Camisa Nike",
            "slug": "camisa-nike",
            "price": 23.99,
            "stock": 20
        }
    }
    
    response = client.post('/product/add', json=new_product)
    product_in_db = db_session.query(ProductModel).filter_by(slug="camisa-nike").first()

    
    body = {
        "name": "Updated camisa",
        "slug": "updated-camisa",
        "price": 23.88,
        "stock": 20
    }
    

    response = client.put(f'/product/update/{product_in_db.id}', json=body)
    
    
    assert response.status_code == status.HTTP_200_OK
    
    new_product_on_db = db_session.query(ProductModel).filter_by(id=product_in_db.id).first()
    db_session.refresh(new_product_on_db)
    
    assert new_product_on_db.name == "Updated camisa"
    assert new_product_on_db.slug == "updated-camisa"
    assert new_product_on_db.price == 23.88
    assert new_product_on_db.stock == 20
    
    db_session.delete(category_model)
    
    db_session.delete(new_product_on_db)
    db_session.commit()

def test_delete_product_route(db_session):
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
    
    response = client.delete(f'/product/delete/{product_on_db.id}')
    
    assert response.status_code == status.HTTP_200_OK
    
    products_on_db = db_session.query(ProductModel).all()
    
    assert len(products_on_db) == 0

def test_list_product_route(db_session):
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
    
    response = client.get('/product/list')
    
    data = response.json()
    
    assert len(data) == 4
    
    assert data[0] == {
        'id': products[0].id,
        'name': products[0].name,
        'slug': products[0].slug,
        'price': products[0].price,
        'stock': products[0].stock,
        'category': {
            'name': products[0].category.name,
            'slug': products[0].category.slug
        }
        
    }
    for product in products:
        db_session.delete(product)
    db_session.commit()
    
    db_session.delete(category)
    db_session.commit()
    
def test_list_product_route_with_search(db_session):
    category = CategoryModel(name='Roupa', slug='roupa')
    db_session.add(category)
    db_session.commit()
    
    products = [ProductModel(name= 'Camisa Nike', slug= 'camisa-nike', price=100.99, stock=20, category_id=category.id),
                ProductModel(name= 'Blusa Nike', slug= 'blusa-nike', price=100.99, stock=20, category_id=category.id),
                ProductModel(name= 'tenis', slug= 'tenis-nike', price=100.99, stock=20, category_id=category.id),
                ProductModel(name= 'Camisa Dc', slug= 'camisa-dc', price=100.99, stock=20, category_id=category.id),
    ]
       
    for product in products:
        db_session.add(product)
    db_session.commit()
    
    for product in products:
        db_session.refresh(product)
    
    response = client.get('/product/list?search=nike')
    
    data = response.json()
    
    assert len(data) == 3
    
    assert data[0] == {
        'id': products[0].id,
        'name': products[0].name,
        'slug': products[0].slug,
        'price': products[0].price,
        'stock': products[0].stock,
        'category': {
            'name': products[0].category.name,
            'slug': products[0].category.slug
        }
        
    }
    for product in products:
        db_session.delete(product)
    db_session.commit()
    
    db_session.delete(category)
    db_session.commit() 