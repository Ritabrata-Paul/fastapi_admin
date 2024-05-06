from fastapi import APIRouter, HTTPException
from typing import List
from models.staff_record import StaffRecord
from pymongo import MongoClient

router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")  # Connect to the MongoDB server
db = client["AdministrativeStaffinfoManager"] 

@router.post("/staff_record/add", response_model=StaffRecord)
async def add_staff_record(record: StaffRecord):
    if db["staff_records"].find_one({"staff_id": record.staff_id}):
        raise HTTPException(status_code=400, detail="Staff record already exists")
    db["staff_records"].insert_one(record.dict())
    return record

@router.put("/staff_record/update/{staff_id}", response_model=StaffRecord)
async def update_staff_record(staff_id: str, record: StaffRecord):
    if not db["staff_records"].find_one({"staff_id": staff_id}):
        raise HTTPException(status_code=404, detail="Staff record not found")
    db["staff_records"].update_one({"staff_id": staff_id}, {"$set": record.dict()})
    return record

@router.get("/staff_record/retrieve/{staff_id}", response_model=StaffRecord)
async def retrieve_staff_record(staff_id: str):
    record = db["staff_records"].find_one({"staff_id": staff_id})
    if not record:
        raise HTTPException(status_code=404, detail="Staff record not found")
    return record

@router.delete("/staff_record/remove/{staff_id}")
async def remove_staff_record(staff_id: str):
    record = db["staff_records"].find_one({"staff_id": staff_id})
    if not record:
        raise HTTPException(status_code=404, detail="Staff record not found")
    db["staff_records"].delete_one({"staff_id": staff_id})
    return {"message": "Staff record removed"}