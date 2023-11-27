from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from decouple import config as decouple_config

from blob.save_blob import save_in_blob
from nosql.database import collection

SECRET_KEY = decouple_config('SECRET_KEY')
ALGORITHM = decouple_config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db = collection


class UserFields(BaseModel):
    username: str
    email: str
    password: str
    points: int = 0
    logged: bool = False


class LoginUserFields(BaseModel):
    username: str
    password: str


class PointFields(BaseModel):
    username: str
    points: int


class GetPoints(BaseModel):
    username: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

origins = ["*", "https://api-casa-do-tatu.onrender.com","apidacasadotatu.azurewebsites.net"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str, email: str, db=db):
    queryName = collection.find_one({"username": username})
    queryEmail = collection.find_one({"email": email})
    if queryName is None:
        if queryEmail is None:
            return None
    user_data = queryName or queryEmail
    return UserFields(**user_data)


def find_user(username: str, db=collection):
    queryName = collection.find_one({"username": username})
    if queryName is None:
        return None
    user_data = queryName
    return UserFields(**user_data)


def authenticate_user(username: str, password: str):
    user = find_user(username, db)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def register_user(user: UserFields, db=db):
    user_dict = dict(user)
    user_dict['password'] = get_password_hash(user_dict['password'])
    db.insert_one(user_dict)
    return {"message": "register successful"}


@app.post("/register")
def register(user: UserFields):
    inDB = get_user(user.username, user.email, db)
    if inDB is None:
        print("pre blob")
        response = register_user(user)
        #save_in_blob(user)
        return response
    else:
        return {"message": "Username or email already exists"}


@app.post("/login")
async def login(user: LoginUserFields):
    inDB = authenticate_user(user.username, user.password)
    if inDB is None:
        response = {"message": "cant find this account or wrong credentials"}
        return response
    else:
        return {"message": "logged in"}


@app.post("/points")
async def change_points(fields: PointFields):
    myquery = {"username": f"{fields.username}"}
    newvalues = {"$set": {"points": fields.points}}
    db.update_one(myquery, newvalues)


@app.post("/getpoints")
async def get_points(username: GetPoints):
    myquery = {"username": f"{username.username}"}
    user = db.find_one(myquery)
    if user:
        return user["points"]
    return {"message": "User not found"}


@app.get("/")
async def index():

    return {"message": "success"}
