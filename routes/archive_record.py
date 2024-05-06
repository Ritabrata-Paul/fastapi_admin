from fastapi import APIRouter, HTTPException
from typing import List
from models.archive_record import ArchiveRecord
from pymongo import MongoClient

router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")  # Connect to the MongoDB server
db = client["StudentArchiveHistory"] 

@router.post("/archive_record/add", response_model=ArchiveRecord)
async def add_archive_record(record: ArchiveRecord):
    if db["archive_records"].find_one({"record_id": record.record_id}):
        raise HTTPException(status_code=400, detail="Record already exists")
    db["archive_records"].insert_one(record.dict())
    return record

@router.put("/archive_record/update/{record_id}", response_model=ArchiveRecord)
async def update_archive_record(record_id: str, record: ArchiveRecord):
    if not db["archive_records"].find_one({"record_id": record_id}):
        raise HTTPException(status_code=404, detail="Record not found")
    db["archive_records"].update_one({"record_id": record_id}, {"$set": record.dict()})
    return record

@router.get("/archive_record/retrieve/{student_id}", response_model=List[ArchiveRecord])
async def retrieve_archive_record(student_id: str):
    records = db["archive_records"].find({"student_id": student_id})
    if records:
        return list(records)
    else:
        raise HTTPException(status_code=404, detail="Record not found")