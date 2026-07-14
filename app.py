from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Product
from models import Inventory
from models import Warehouse
from models import Supplier
from sqlalchemy import func


app = FastAPI(
    title="Warehouse Inventory API",
    servers=[
        {
            "url": "https://warehouse-inventory-assistant.onrender.com",
            "description": "Production server"
        }
    ]
)


@app.get("/")
def home():

    return {

        "message": "Warehouse API is running"

    }


@app.get("/inventory/stock")
def get_product_stock(product_name: str):

    db: Session = SessionLocal()

    try:

        results = (

            db.query(

                Product.product_name,

                Warehouse.warehouse_name,

                Inventory.available_stock,

                Inventory.reserved_stock,

                Inventory.rack

            )

            .join(

                Inventory,

                Product.product_id == Inventory.product_id

            )

            .join(

                Warehouse,

                Inventory.warehouse_id == Warehouse.warehouse_id

            )

            .filter(

                Product.product_name.ilike(

                    f"%{product_name}%"

                )

            )

            .all()

        )

        response = []

        for row in results:

            response.append(

                {

                    "product_name": row.product_name,

                    "warehouse": row.warehouse_name,

                    "available_stock": row.available_stock,

                    "reserved_stock": row.reserved_stock,

                    "rack": row.rack

                }

            )

        return response

    finally:

        db.close()

from models import Product


@app.get("/products/search")
def search_products(
    keyword: str = None,
    brand: str = None,
    category: str = None
):

    db: Session = SessionLocal()

    try:

        query = db.query(
            Product.product_id,
            Product.product_name,
            Product.brand,
            Product.category,
            Product.price,
            Product.reorder_level
        )

        if keyword:

            query = query.filter(
                Product.product_name.ilike(
                    f"%{keyword}%"
                )
            )

        if brand:

            query = query.filter(
                Product.brand.ilike(
                    f"%{brand}%"
                )
            )

        if category:

            query = query.filter(
                Product.category.ilike(
                    f"%{category}%"
                )
            )

        results = query.all()

        response = []

        for row in results:

            response.append(

                {

                    "product_id": row.product_id,

                    "product_name": row.product_name,

                    "brand": row.brand,

                    "category": row.category,

                    "price": float(row.price),

                    "reorder_level": row.reorder_level

                }

            )

        return response

    finally:

        db.close()

@app.get("/inventory/location")
def get_product_location(product_name: str):

    db: Session = SessionLocal()

    try:

        results = (

            db.query(

                Product.product_name,

                Warehouse.warehouse_name,

                Warehouse.city,

                Inventory.rack,

                Inventory.available_stock

            )

            .join(

                Inventory,

                Product.product_id == Inventory.product_id

            )

            .join(

                Warehouse,

                Inventory.warehouse_id == Warehouse.warehouse_id

            )

            .filter(

                Product.product_name.ilike(

                    f"%{product_name}%"

                )

            )

            .all()

        )

        response = []

        for row in results:

            response.append(

                {

                    "product_name": row.product_name,

                    "warehouse": row.warehouse_name,

                    "city": row.city,

                    "rack": row.rack,

                    "available_stock": row.available_stock

                }

            )

        return response

    finally:

        db.close()



@app.get("/suppliers/details")
def get_supplier_details(product_name: str):

    db: Session = SessionLocal()

    try:

        results = (

            db.query(

                Product.product_name,

                Product.brand,

                Supplier.supplier_name,

                Supplier.contact_email,

                Supplier.phone

            )

            .join(

                Supplier,

                Product.supplier_id == Supplier.supplier_id

            )

            .filter(

                Product.product_name.ilike(

                    f"%{product_name}%"

                )

            )

            .all()

        )

        response = []

        for row in results:

            response.append(

                {

                    "product_name": row.product_name,

                    "brand": row.brand,

                    "supplier_name": row.supplier_name,

                    "contact_email": row.contact_email,

                    "phone": row.phone

                }

            )

        return response

    finally:

        db.close()

@app.get("/inventory/low-stock")
def get_low_stock_items(
    warehouse: str = None,
    category: str = None
):

    db: Session = SessionLocal()

    try:

        query = (

            db.query(

                Product.product_name,

                Product.brand,

                Product.category,

                Warehouse.warehouse_name,

                Inventory.available_stock,

                Product.reorder_level

            )

            .join(

                Inventory,

                Product.product_id == Inventory.product_id

            )

            .join(

                Warehouse,

                Inventory.warehouse_id == Warehouse.warehouse_id

            )

        )

        if warehouse:

            query = query.filter(

                Warehouse.city.ilike(

                    f"%{warehouse}%"

                )

            )

        if category:

            query = query.filter(

                Product.category.ilike(

                    f"%{category}%"

                )

            )

        query = query.filter(

            Inventory.available_stock < Product.reorder_level

        )

        results = query.all()

        response = []

        for row in results:

            response.append(

                {

                    "product_name": row.product_name,

                    "brand": row.brand,

                    "category": row.category,

                    "warehouse": row.warehouse_name,

                    "available_stock": row.available_stock,

                    "reorder_level": row.reorder_level

                }

            )

        return response

    finally:

        db.close()


@app.get("/inventory/statistics")
def get_inventory_statistics(
    metric: str,
    warehouse: str = None
):

    db: Session = SessionLocal()

    try:

        query = (

            db.query(

                Product.product_name,

                Warehouse.warehouse_name,

                Inventory.available_stock

            )

            .join(

                Inventory,

                Product.product_id == Inventory.product_id

            )

            .join(

                Warehouse,

                Inventory.warehouse_id == Warehouse.warehouse_id

            )

        )

        if warehouse:

            query = query.filter(

                Warehouse.city.ilike(

                    f"%{warehouse}%"

                )

            )

        if metric == "highest_stock":

            result = (

                query

                .order_by(

                    Inventory.available_stock.desc()

                )

                .first()

            )

            return {

                "product_name": result.product_name,

                "warehouse": result.warehouse_name,

                "stock": result.available_stock

            }

        elif metric == "lowest_stock":

            result = (

                query

                .order_by(

                    Inventory.available_stock.asc()

                )

                .first()

            )

            return {

                "product_name": result.product_name,

                "warehouse": result.warehouse_name,

                "stock": result.available_stock

            }

        elif metric == "average_stock":

            avg = (

                db.query(

                    func.avg(

                        Inventory.available_stock

                    )

                )

                .scalar()

            )

            return {

                "average_stock": round(avg, 2)

            }

        elif metric == "top_products":

            results = (

                query

                .order_by(

                    Inventory.available_stock.desc()

                )

                .limit(10)

                .all()

            )

            return [

                {

                    "product_name": r.product_name,

                    "warehouse": r.warehouse_name,

                    "stock": r.available_stock

                }

                for r in results

            ]

        elif metric == "warehouse_stock":

            results = (

                db.query(

                    Warehouse.warehouse_name,

                    func.sum(

                        Inventory.available_stock

                    )

                )

                .join(

                    Inventory,

                    Warehouse.warehouse_id == Inventory.warehouse_id

                )

                .group_by(

                    Warehouse.warehouse_name

                )

                .all()

            )

            return [

                {

                    "warehouse": r[0],

                    "total_stock": r[1]

                }

                for r in results

            ]

        else:

            return {

                "error": "Invalid metric"

            }

    finally:

        db.close()