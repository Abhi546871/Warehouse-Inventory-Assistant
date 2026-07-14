from database import SessionLocal
from models import Product

db = SessionLocal()

products = db.query(Product).limit(5).all()

for product in products:
    print(
        product.product_id,
        product.product_name,
        product.brand
    )

db.close()