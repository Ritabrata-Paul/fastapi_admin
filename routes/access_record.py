from fastapi import APIRouter, HTTPException
from typing import List
from models.access_record import AccessRecord
from pymongo import MongoClient

router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")  # Connect to the MongoDB server
db = client["AccessControllerDatabase"] 

@router.post("/access_record/grant", response_model=AccessRecord)
async def grant_access(record: AccessRecord):
    if db["access_records"].find_one({"user_id": record.user_id, "resource_id": record.resource_id}):
        raise HTTPException(status_code=400, detail="Access already granted")
    record.access_status = True
    db["access_records"].insert_one(record.dict())
    return record

@router.post("/access_record/revoke/{user_id}/{resource_id}")
async def revoke_access(user_id: str, resource_id: str):
    record = db["access_records"].find_one({"user_id": user_id, "resource_id": resource_id})
    if not record:
        raise HTTPException(status_code=404, detail="Access record not found")
    record["access_status"] = False
    db["access_records"].update_one({"user_id": user_id, "resource_id": resource_id}, {"$set": record})
    return {"message": "Access revoked"}

@router.get("/access_record/check/{user_id}/{resource_id}", response_model=AccessRecord)
async def check_access(user_id: str, resource_id: str):
    record = db["access_records"].find_one({"user_id": user_id, "resource_id": resource_id})
    if not record:
        raise HTTPException(status_code=404, detail="Access record not found")
    return record