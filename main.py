from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/url")
async def root():
    return {"url": "https://twitter.com/WilmerFabianT"}



# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL + C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc

# Cliente Peticiones en VSC: ThunderClient