from fastapi import FastAPI
from whitelist.routes import router as whitelist_router

app = FastAPI()
app.include_router(whitelist_router, prefix="/whitelist")