from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes.auth import auth as auth
from app.api.v1.routes.jobseeker import UserProfile as UserProfile
from app.api.v1.routes.recruiter import recruiter as recruiter

app = FastAPI()

origins = [
    "https://job-portal-reactjs.netlify.app",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(UserProfile.router)
app.include_router(recruiter.router)