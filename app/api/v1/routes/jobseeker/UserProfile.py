from fastapi import Request, Form, UploadFile, File, APIRouter, Depends, HTTPException, Query, status
from pydantic import  Field
from app.services.jobseeker_service import create_user_profile, update_user_profile, get_all_jobs, get_job_by_id, apply_on_job, get_my_applications, user_profile_details
from app.schemas.UserProfile import UserProfile
from app.db.session import SessionLocal
from app.utils.util import verify_token, get_user_required_field
from app.schemas.Applications import ApplicationSchema


router = APIRouter(
    prefix="/job",
    tags=["profile"],
    responses={404: {"description": "Not found"}}
)

@router.post("/{userid}")
async def create_profile(userid: str, 
    user_profile: UserProfile, 
    user_email: str = Depends(get_user_required_field), 
    token: dict = Depends(verify_token)):
    db = SessionLocal()
    token_sub = token.get("sub", "")
    return create_user_profile(userid, user_profile, user_email, db, token_sub)

@router.put("/{userid}")
async def update_profile(userid : str, 
user_profile : UserProfile, 
user_email: str = Depends(get_user_required_field),
token: dict = Depends(verify_token)
):
    db = SessionLocal()
    token_sub = token.get("sub", "")
    return update_user_profile(userid, user_profile, user_email, db, token_sub)
    
    
@router.get("/")
async def get_jobs():
    db = SessionLocal()
    return get_all_jobs(db)


@router.get("/{jobid}")
async def get_this_job(jobid : str):
    db = SessionLocal()
    return get_job_by_id(jobid, db)

@router.post("/apply/{jobid}", response_model=ApplicationSchema)
async def apply(
    jobid: int,
    minYearsOfExperience: str = Form(...),
    resumeLink: UploadFile = File(...),
    token: dict = Depends(verify_token)
): 
    db = SessionLocal()
    print("m ",type(resumeLink))
    return apply_on_job(jobid, minYearsOfExperience, resumeLink, token, db)


@router.get("/applications/{userid}")
async def get_applications(userid : int, token: dict = Depends(verify_token)):
    db = SessionLocal()
    return get_my_applications(userid, db)

@router.get("/user-profile/{userid}")
async def userprofile(userid : int, token: dict = Depends(verify_token)):
    db = SessionLocal()
    token_sub = token.get("sub", "")
    return user_profile_details(userid, token_sub, db)

    