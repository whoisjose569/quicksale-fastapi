from fastapi import FastAPI
from routes.category_routes import router as category_routes
from routes.product_routes import router as product_routes
from routes.user_routes import router as user_routes

app = FastAPI()

@app.get('/health-check')
def health_check():
    return True

app.include_router(category_routes)
app.include_router(product_routes)
app.include_router(user_routes)