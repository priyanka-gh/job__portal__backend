from datetime import datetime
from fastapi import HTTPException, status
import os
from app.db.models.Applications import Application
from app.db.models.Users import User
from app.db.models.Jobs import Jobs


def create_a_job(recruiter_id, job_desc, db):
    user = db.query(User).filter(User.userid == recruiter_id).first()
    try:
        current_time = datetime.utcnow()
        new_job = Jobs(title = job_desc.title, 
        jobDescription = job_desc.jobDescription, 
        minYearsOfExperience = job_desc.minYearsOfExperience, 
        category = job_desc.category, 
        lastDateToRegister = job_desc.lastDateToRegister, 
        companyName = job_desc.companyName, 
        companyDescription = job_desc.companyDescription, 
        postedBy = user.email,
        postedAt = current_time,
        updatedAt = current_time,
        active = job_desc.active,
        stipend = job_desc.stipend,
        )
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return {
            "jobid" : new_job.jobid,
            "title": new_job.title,
            "jobDescription": new_job.jobDescription,
            "minYearsOfExperience": new_job.minYearsOfExperience,
            "category": new_job.category,
            "lastDateToRegister": new_job.lastDateToRegister,
            "companyName": new_job.companyName,
            "companyDescription": new_job.companyDescription,
            "postedBy": new_job.postedBy,
            "postedAt" : new_job.postedAt,
            "updatedAt": new_job.updatedAt,
            "active" : new_job.active,
            "stipend" : new_job.stipend
        }
    
    except Exception as e:
            db.rollback()
            print(str(e))
            raise HTTPException(status_code=500, detail=str(e))


def update_a_job(jobid, job_desc, token_sub: str, db):
    job = db.query(Jobs).filter(Jobs.jobid == jobid).first()
    
    current_time = datetime.utcnow()

    try:
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
    except HTTPException as e:
        raise

    try:
        userid = db.query(User).filter(User.email == job.postedBy).first()
        userid = str(userid.userid)
        if token_sub != userid:
            raise HTTPException(status_code=403, detail="Token user does not match requested user")
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    try:

        job.title = job_desc.title
        job.jobDescription = job_desc.jobDescription
        job.minYearsOfExperience = job_desc.minYearsOfExperience
        job.category = job_desc.category
        job.lastDateToRegister = job_desc.lastDateToRegister
        job.companyName = job_desc.companyName
        job.companyDescription = job_desc.companyDescription
        job.postedBy = job.postedBy
        job.postedAt = job.postedAt
        job.updatedAt = current_time
        job.active = job_desc.active

        db.commit()
        db.refresh(job)

        return {
            "title": job.title,
            "jobDescription": job.jobDescription,
            "minYearsOfExperience": job.minYearsOfExperience,
            "category": job.category,
            "lastDateToRegister": job.lastDateToRegister,
            "companyName": job.companyName,
            "co mpanyDescription": job.companyDescription,
            "postedBy": job.postedBy,
            "postedAt" : job.postedAt,
            "updatedAt": job.updatedAt,
            "active" : job.active
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def delete_a_job(jobid, token_sub: str, db):
    job = db.query(Jobs).filter(Jobs.jobid == jobid).first()
    print(job.jobid)
    try:
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
    except HTTPException as e:
        print(str(e))

    try:
        userid = db.query(User).filter(User.email == job.postedBy).first().userid
        userid = str(userid)
        if token_sub != userid:
            raise HTTPException(status_code=403, detail="Token user does not match requested user")
    except HTTPException as e:
        print(str(e))


    try:
        db.delete(job)
        db.commit()
        return {"message" : "Sucessfully deleted"}
    except Exception as e:
        print(str(e))
        db.rollback()
        # raise HTTPException(status_code=500, detail=str(e))
    

def get_all_jobs(token_sub : str, db, page: int = 1, per_page: int = 10):
    try:
        offset = (page - 1) * per_page if page > 1 else 0
        jobs = db.query(Jobs).filter(Jobs.postedBy == token_sub).offset(offset).limit(per_page).all()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_a_job(jobid : str, token : dict, db):
    job = db.query(Jobs).filter(Jobs.jobid == jobid).first()
    
    try:
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
    except HTTPException as e:
        raise
    
    try:
        if token.get("email") != job.postedBy:
            raise HTTPException(status_code=403, detail="Token user does not match requested user")
    except HTTPException as e:
        raise
    
    try:
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def change_application_status(jobid : int, applicationid : int, userapplication, email : str, db):
    job_posted_by = db.query(Jobs).filter(Jobs.jobid == jobid).first()
    job_posted_by = job_posted_by.postedBy

    try:
        if email == job_posted_by:
            application = db.query(Application).filter(Application.applicationid == applicationid).first()
            application.status = userapplication.status
            db.commit()
            db.refresh(application)

            return{
            "firstName": application.firstName,
            "middleName": application.middleName,
            "lastName": application.lastName,
            "phone": application.phone,
            "email": application.email,
            "resumeLink": application.resumeLink,
            "status": application.status
            } 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))



def get_all_applicants(jobid, db):
    try:
        all_applicants = db.query(Application).filter(Application.jobId == jobid).all()
        return all_applicants
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))