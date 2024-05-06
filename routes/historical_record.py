from fastapi import APIRouter, HTTPException
from typing import List
from models.historical_record import HistoricalRecord
from pymongo import MongoClient

router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")  # Connect to the MongoDB server
db = client["Studenthistoricalrecordmanagerdatabase"] 

@router.post("/historical_record/add", response_model=HistoricalRecord)
async def add_historical_record(record: HistoricalRecord):
    if db["historical_records"].find_one({"student_id": record.student_id}):
        raise HTTPException(status_code=400, detail="Record already exists")
    db["historical_records"].insert_one(record.dict())
    return record

@router.put("/historical_record/update", response_model=HistoricalRecord)
async def update_historical_record(record: HistoricalRecord):
    if not db["historical_records"].find_one({"student_id": record.student_id}):
        raise HTTPException(status_code=404, detail="Record not found")
    db["historical_records"].update_one({"student_id": record.student_id}, {"$set": record.dict()})
    return record

@router.get("/historical_record/retrieve/{student_id}", response_model=HistoricalRecord)
async def retrieve_historical_record(student_id: str):
    record = db["historical_records"].find_one({"student_id": student_id})
    if record:
        return record
    else:
        raise HTTPException(status_code=404, detail="Record not found")