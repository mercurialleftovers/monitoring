from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

db: dict[str, str] = {}
db["kiskiller0"] = "secret0"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# NOTE(bader): set cookie header (Authorization: Bearrer something), and visit /secure
@app.get("/")
async def home():
    return {"home": "sweet home"}


@app.get("/secure/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
