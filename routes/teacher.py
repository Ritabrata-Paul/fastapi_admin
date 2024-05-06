from fastapi import APIRouter, HTTPException
from typing import List
from models.teacher import Teacher
from pymongo import MongoClient

router = APIRouter()


client = MongoClient("mongodb://localhost:27017/")  # Connect to the MongoDB server
db = client["TeacherInfoManagerDatabase"] 


# from some_module import get_teacher_courses, get_teacher_schedule

@router.post("/teacher/add", response_model=Teacher)
async def add_teacher(teacher: Teacher):
    if db["teachers"].find_one({"teacher_id": teacher.teacher_id}):
        raise HTTPException(status_code=400, detail="Teacher already exists")
    db["teachers"].insert_one(teacher.dict())
    return teacher

@router.put("/teacher/update/{teacher_id}", response_model=Teacher)
async def update_teacher(teacher_id: str, teacher: Teacher):
    if not db["teachers"].find_one({"teacher_id": teacher_id}):
        raise HTTPException(status_code=404, detail="Teacher not found")
    db["teachers"].update_one({"teacher_id": teacher_id}, {"$set": teacher.dict()})
    return teacher

@router.get("/teacher/retrieve/{teacher_id}", response_model=Teacher)
async def retrieve_teacher(teacher_id: str):
    teacher = db["teachers"].find_one({"teacher_id": teacher_id})
    if teacher:
        return teacher
    else:
        raise HTTPException(status_code=404, detail="Teacher not found")