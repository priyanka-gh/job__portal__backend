from app.services.recruiter_service import create_a_job,update_a_job, delete_a_job, get_all_jobs, get_a_job, change_application_status, get_all_applicants
from fastapi import Request, Form, APIRouter, Depends, HTTPException, Query, status
from app.schemas.Jobs import Jobs
from app.schemas.Applications import ApplicationSchema
from app.db.session import SessionLocal
from app.utils.util import verify_token, get_user_required_field, check_user_role

router = APIRouter(
    prefix="/recruiter",
    tags=["recruiter"],
    dependencies=[Depends(check_user_role)],
    responses={404: {"description": "Not found"}}
)

@router.post("/job")
async def create_job(job_desc : Jobs, token: dict = Depends(verify_token)):
    db = SessionLocal()

    recruiter_id = token.get("sub")
    return create_a_job(recruiter_id, job_desc, db)
    
@router.put("/job/{jobid}")
async def update_job(jobid : str, job_desc : Jobs, token: dict = Depends(verify_token)):
    db = SessionLocal()
    token_sub = token.get("sub")
    return update_a_job(jobid, job_desc, token_sub, db)


@router.delete("/job/{jobid}")
async def delete_job(jobid : str, token: dict = Depends(verify_token)):
    db = SessionLocal()
    token_sub = token.get("sub")
    return delete_a_job(jobid, token_sub, db)
    

@router.get("/job")
async def get_jobs(page : int = Query(1, description = "Page number", gt = 0), per_page: int = Query(10, description = "Items per page"), token: dict = Depends(verify_token)):
    db = SessionLocal()
    token_sub = token.get("email")
    return get_all_jobs(token_sub, db, page, per_page)


@router.get("/job/{jobid}")
async def get_jobs(jobid : str,token: dict = Depends(verify_token)):
    db = SessionLocal()
    return get_a_job(jobid, token, db)


@router.put("/job/{jobid}/applications/{applicationid}")
async def change_app_status(jobid : int, applicationid : int, application : ApplicationSchema, token: dict = Depends(verify_token)):
    print("app",application)
    db = SessionLocal()
    email = token.get("email")
    return change_application_status(jobid, applicationid, application, email, db)

@router.get("/job/{jobid}/applicants")
async def get_applicants(jobid : int, token: dict = Depends(verify_token)):
    db = SessionLocal()
    return get_all_applicants(jobid, db)