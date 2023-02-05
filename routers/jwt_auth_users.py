from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = '97a770d68afc75a8aae3a5e4a8b3f638dded29d1b3faa465897cd0fbb6c7a939'

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str 
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    'wilmertri': {
        'username': 'wilmertri',
        'full_name': 'Wilmer Triana',
        'email': 'wilmerfabiantriana@outlook.com',
        'disabled': False,
        'password': '$2a$12$yabaB7BF1pWbFpat.OK8qet3Ek0tcbdS9peLxWNUKxewxY2LKB4B2'
    },
    'fabiantri': {
        'username': 'fabiantri',
        'full_name': 'Fabian Triana',
        'email': 'fabiantriana1072@gmail.com',
        'disabled': True,
        'password': '$2a$12$Djo.dhQhbkx9z4WMa/l4seM5gym4I3Ck.VPh/AmC.70xeWyB7JBQW'
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

@router.post("/login/jwt")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {
        "sub":user.username, 
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación invalidas", 
            headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception 
    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")

    return user


@router.get("/jwt/users/me")
async def me(user: User = Depends(current_user)):
    return user