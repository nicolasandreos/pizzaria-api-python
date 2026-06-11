from fastapi import FastAPI
from routes.auth_router import auth_router
from routes.order_router import order_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)

# Para rodar a aplicação, use o comando: uvicorn main:app --reload