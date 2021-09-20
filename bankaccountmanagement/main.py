from fastapi import FastAPI
from bankaccountmanagement import models
from bankaccountmanagement.database import engine
from bankaccountmanagement.routers import user
from bankaccountmanagement.routers import account
from bankaccountmanagement.routers import service


# Initialize FastAPI
app = FastAPI()

# Generate all models in DB when server is started 
models.Base.metadata.create_all(engine)

# Add Routers
app.include_router(user.router)
app.include_router(account.router)
app.include_router(service.router)
