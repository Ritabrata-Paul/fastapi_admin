from fastapi import FastAPI, Request
from pymongo import MongoClient
from passlib.context import CryptContext  # For secure password hashing
# from routes.user import user_router 
from fastapi.templating import Jinja2Templates

from routes.user import router as user_account_router # Import user router
from routes import historical_record
from routes.archive_record import router as archive_record_router
from routes.staff_record import router as staff_record_router
from routes.access_record import router as access_record_router
from routes.programme import router as programme_router
from routes.student import router as student_router
from routes.teacher import router as teacher_router
from fastapi.responses import FileResponse, HTMLResponse

# Connection and setup (unchanged from previous examples)

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Password hashing context
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
  return FileResponse("index.html")

@app.get("/register", response_class=HTMLResponse)
async def read_register():
    return FileResponse("register.html")

@app.get("/login", response_class=HTMLResponse)
async def read_login():
    return FileResponse("login.html")

@app.get("/profile", response_class=HTMLResponse)
async def read_profile():
    return FileResponse("profile.html")



# app.include_router(user_router, tags=["User_Registration"])
app.include_router(user_account_router, tags=["user_accounts"])
app.include_router(historical_record.router, tags=["historical_record"])
app.include_router(archive_record_router, prefix="/archive_records", tags=["archive_records"])
app.include_router(staff_record_router, prefix="/staff_records", tags=["staff_records"])
app.include_router(access_record_router, prefix="/access_records", tags=["access_records"])
app.include_router(programme_router, prefix="/programmes", tags=["programmes"])
app.include_router(student_router, prefix="/students", tags=["students"])
app.include_router(teacher_router, prefix="/teachers", tags=["teachers"])