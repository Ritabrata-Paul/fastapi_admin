import logging
import requests
from fastapi import APIRouter, HTTPException
from typing import List
from models.student import Student, ArchiveRecordSummary
from models.archive_record import ArchiveRecord
from pymongo import MongoClient

router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")  # Connect to the MongoDB server
db = client["StudentInformationManagerDatabase"] 

@router.post("/student/add", response_model=Student)
async def add_student(student: Student):
    if db["students"].find_one({"student_id": student.student_id}):
        raise HTTPException(status_code=400, detail="Student already exists")
    db["students"].insert_one(student.dict())
    return student

@router.put("/student/update/{student_id}", response_model=Student)
async def update_student(student_id: str, student: Student):
    if not db["students"].find_one({"student_id": student_id}):
        raise HTTPException(status_code=404, detail="Student not found")
    db["students"].update_one({"student_id": student_id}, {"$set": student.dict()})
    return student

# @router.get("/student/{student_id}/archive_records", response_model=List[ArchiveRecord])
# async def retrieve_student_archive_records(student_id: str):
#     records = db["archive_records"].find({"student_id": student_id}, {"course_id": 1, "grade": 1, "_id": 0})
#     if records:
#         return list(records)
#     else:
#         raise HTTPException(status_code=404, detail="Record not found")


# @router.get("/archive_record/retrieve/{student_id}", response_model=List[ArchiveRecord])
# async def retrieve_archive_record(student_id: str):
#     records = db["archive_records"].find({"student_id": student_id})
#     if records:
#         return list(records)
#     else:
#         raise HTTPException(status_code=404, detail="Record not found")
    
@router.get("/archive_record/retrieve/{student_id}", response_model=List[ArchiveRecordSummary])
async def retrieve_archive_record(student_id: str):
    records = db["StudentArchiveHistory"].find({"student_id": student_id}, {"course_id": 1, "grade": 1, "_id": 0})
    if records:
        return list(records)
    else:
        raise HTTPException(status_code=404, detail="Record not found")
