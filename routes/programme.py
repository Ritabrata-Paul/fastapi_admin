import requests

from fastapi import APIRouter, HTTPException
from typing import List
from models.programme import Programme, Course
from pymongo import MongoClient

router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")  # Connect to the MongoDB server
db = client["ProgrammeAndModuleManager"] 

@router.post("/programme/add", response_model=Programme)
async def add_programme(programme: Programme):
    if db["programmes"].find_one({"programme_id": programme.programme_id}):
        raise HTTPException(status_code=400, detail="Programme already exists")
    db["programmes"].insert_one(programme.dict())
    return programme

@router.put("/programme/update/{programme_id}", response_model=Programme)
async def update_programme(programme_id: str, programme: Programme):
    if not db["programmes"].find_one({"programme_id": programme_id}):
        raise HTTPException(status_code=404, detail="Programme not found")
    db["programmes"].update_one({"programme_id": programme_id}, {"$set": programme.dict()})
    return programme

@router.get("/programme/retrieve/{programme_id}", response_model=Programme)
async def retrieve_programme(programme_id: str):
    programme = db["programmes"].find_one({"programme_id": programme_id})
    if not programme:
        raise HTTPException(status_code=404, detail="Programme not found")
    return programme

@router.post("/programme/{programme_id}/add_course", response_model=Programme)
async def add_course_to_programme(programme_id: str, course: Course):
    programme = db["programmes"].find_one({"programme_id": programme_id})
    if not programme:
        raise HTTPException(status_code=404, detail="Programme not found")
    if "courses" not in programme:
        programme["courses"] = []
    programme["courses"].append(course.dict())
    db["programmes"].update_one({"programme_id": programme_id}, {"$set": programme})
    return programme
