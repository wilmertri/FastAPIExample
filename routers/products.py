from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/products", 
                    tags=["products"], 
                    responses={404: {"message":"Not founded"}})

# Entity Product

class Product(BaseModel):
    id: int
    name: str 

products_list = [Product(id=1, name="Product 1"),Product(id=2, name="Product 2"),Product(id=3, name="Product 3")]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]