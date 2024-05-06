from fastapi import APIRouter, HTTPException
from typing import List
from models.user import UserAccount
from passlib.context import CryptContext
from pymongo import MongoClient  # For secure password hashing
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Password hashing context


client = MongoClient("mongodb://localhost:27017/")  # Connect to the MongoDB server
db = client["UniversityAccountManager"]  # Connect to the "University Account Manager" database


@router.post("/user_account/register", response_model=UserAccount)
async def register_user_account(account: UserAccount):
    if db["user_accounts"].find_one({"user_id": account.user_id}):
        raise HTTPException(status_code=400, detail="User account already exists")
    account.password = pwd_context.hash(account.password)  # Hash the password
    db["user_accounts"].insert_one(account.dict())
    return account

@router.post("/user_account/authenticate")
async def authenticate_user_account(user_id: str, password: str):
    account = db["user_accounts"].find_one({"user_id": user_id})
    if not account or not pwd_context.verify(password, account["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Authenticated successfully"}

@router.put("/user_account/update/{user_id}", response_model=UserAccount)
async def update_user_account(user_id: str, account: UserAccount):
    if not db["user_accounts"].find_one({"user_id": user_id}):
        raise HTTPException(status_code=404, detail="User account not found")
    account.password = pwd_context.hash(account.password)  # Hash the new password
    db["user_accounts"].update_one({"user_id": user_id}, {"$set": account.dict()})
    return account


