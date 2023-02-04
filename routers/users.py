from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Inicia el server: uvicorn users:app --reload

# Entidad user

class User(BaseModel):
    id: int
    name: str 
    surname: str
    url: str
    age: int

users_list = [User(id=1,name="Fabian",surname="Triana", url="https://twitter.com/WilmerFabianT",age=31),
                User(id=2,name="William",surname="Dev",url="https://twitter.com/WilDev",age=25)]

@router.get("/usersjson")
async def usersjson():
    return [{"name": "Fabian", "surmane":"Triana", "url":"https://twitter.com/WilmerFabianT", "age":31},
            {"name": "William", "surmane":"Dev", "url":"https://twitter.com/WillDev", "age":25}]

@router.get("/users")
async def users():
    return users_list

#Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

#Query
@router.get("/user/")
async def user(id: int):
    return search_user(id)

@router.post("/user", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    
    users_list.append(user)
    return user

@router.put("/user")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "No sé ha actualizado el usuario"}
    
    return user

@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "No sé ha eliminado el usuario"}
    
    return {"success": "El usuario sé ha eliminado"}

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No sé ha encontrado el usuario"}

