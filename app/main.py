
from fastapi import FastAPI
from app.presentation.routers import auth_router, address_router

app = FastAPI(title="Base FastAPI Project")

app.include_router(auth_router.router)
app.include_router(address_router.router)

@app.get("/")
def read_root():
    return {"message": "API Base Online! Acesse /docs"}