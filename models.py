from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Supplier(Base):

    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True)
    supplier_name = Column(String)
    contact_email = Column(String)
    phone = Column(String)


class Warehouse(Base):

    __tablename__ = "warehouses"

    warehouse_id = Column(Integer, primary_key=True)
    warehouse_name = Column(String)
    city = Column(String)
    address = Column(String)


class Product(Base):

    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    brand = Column(String)
    category = Column(String)

    price = Column(DECIMAL)

    reorder_level = Column(Integer)

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.supplier_id")
    )


class Inventory(Base):

    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True)

    product_id = Column(
        Integer,
        ForeignKey("products.product_id")
    )

    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.warehouse_id")
    )

    available_stock = Column(Integer)

    reserved_stock = Column(Integer)

    rack = Column(String)

    date_added = Column(Date)