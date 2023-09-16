from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.db.models.UserProfile import UserProfile
from app.db.models.Users import User
from app.db.models.Jobs import Jobs
from app.db.models.Applications import Application
from app.utils.util import exists_with_filters, upload_resume

def create_user_profile(userid: str, user_profile, user_email, db, token_sub: str):
    user = db.query(User).filter(User.userid == userid).first()

    try:
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException as e:
        raise

    try:
        if token_sub != userid:
            raise HTTPException(status_code=403, detail="Token user does not match requested user")
    except HTTPException as e:
        raise

    try:
        if exists_with_filters(db, UserProfile, "email", user_email):
            raise HTTPException(status_code=409, detail="Profile already exists")
    except HTTPException as e:
        raise
    
    try:
        user_profile_entry = UserProfile(
            userId=user.userid,
            firstName=user_profile.firstName,
            middleName=user_profile.middleName,
            lastName=user_profile.lastName,
            email=user.email,
            phone=user_profile.phone,
            roleTitle=user_profile.roleTitle
        )

        db.add(user_profile_entry)
        db.commit()
        db.refresh(user_profile_entry)

        return {
            "firstName": user_profile_entry.firstName,
            "middleName": user_profile_entry.middleName,
            "lastName": user_profile_entry.lastName,
            "phone": user_profile_entry.phone,
            "email": user_profile_entry.email,
            "roleTitle": user_profile_entry.roleTitle
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")



def update_user_profile(userid: str, user_profile: UserProfile, user_email: str, db, token_sub: str):
    user_profile_entry = db.query(UserProfile).filter(UserProfile.userId == userid).first()

    try:
        if token_sub != userid:
            raise HTTPException(status_code=403, detail="Token user does not match requested user")
    except HTTPException as e:
        raise

    try:
        if not user_profile_entry:
            raise HTTPException(status_code=403, detail="Profile not found")
    except HTTPException as e:
        raise
            
    try:
        user_profile_entry.firstName = user_profile.firstName
        user_profile_entry.middleName = user_profile.middleName
        user_profile_entry.lastName = user_profile.lastName
        user_profile_entry.phone = user_profile.phone
        user_profile_entry.roleTitle = user_profile.roleTitle
        db.commit()
        db.refresh(user_profile_entry)
        return {
            "firstName": user_profile_entry.firstName,
            "middleName": user_profile_entry.middleName,
            "lastName": user_profile_entry.lastName,
            "phone": user_profile_entry.phone,
            "email": user_email,
            "roleTitle": user_profile_entry.roleTitle
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_all_jobs(db, page: int = 1, per_page: int = 10):
    try:
        offset = (page - 1) * per_page if page > 1 else 0
        jobs = db.query(Jobs).filter(Jobs.active != 0).offset(offset).limit(per_page).all()
        return jobs
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
        
def get_job_by_id(jobid, db):
    try:
        job = db.query(Jobs).filter(Jobs.jobid == jobid).all()
        return job
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
        
def apply_on_job(
    job_id, 
    minYearsOfExperience, 
    resumeLink, 
    token, 
    db
):
    current_time = datetime.utcnow()
    userid = token.get("sub")
    job = db.query(Jobs).filter(Jobs.jobid == job_id).first()
    user = db.query(UserProfile).filter(UserProfile.userId == userid).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    existing_applicant = db.query(Application).filter(Application.jobId == job_id).first()

    if existing_applicant:
        raise HTTPException(status_code=400, detail="You have already applied for this job")

    if job.active == 0:
        raise HTTPException(status_code=400, detail="No longer accepting applications")

    try:
        resume_link = upload_resume(user.email, resumeLink)
        
        db_application = Application(
            userId = user.userId,
            jobId = job_id,
            firstName=user.firstName,
            middleName=user.middleName,
            lastName=user.lastName,
            email=user.email,
            phone=user.phone,
            minYearsOfExperience=minYearsOfExperience,
            appliedAt=current_time,
            status = "APPLIED"
        )
        db.add(db_application)
        db.commit()
        db.refresh(db_application)

        db_application.resumeLink = resume_link
        db.commit()
        return{
            "firstName": db_application.firstName,
            "middleName": db_application.middleName,
            "lastName": db_application.lastName,
            "phone": db_application.phone,
            "email": db_application.email,
            "resumeLink": resume_link,
            "status": db_application.status,
            "minYearsOfExperience": db_application.minYearsOfExperience
        } 
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


from fastapi import HTTPException

def get_my_applications(userid: int, db):
    try:
        applications_with_company = db.query(Application, Jobs).filter(Application.jobId == Jobs.jobid).filter(Application.userId == userid).all()
        my_applications = []

        for application, job in applications_with_company:
            result = {
                'applicationid': application.applicationid,
                'companyName': job.companyName,
                'jobId' : application.jobId,
                'firstName': application.firstName,
                'middleName': application.middleName,
                'lastName': application.lastName,
                'email' : application.email,
                'phone' : application.phone,
                'status' : application.status,
                'appliedAt' : application.appliedAt,
                'postedBy' : job.postedBy
            }
            my_applications.append(result)

        return my_applications

    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

def user_profile_details(userid : int, token_sub, db):
    try:
        if str(userid) == token_sub:
            user = db.query(UserProfile).filter(UserProfile.userId == userid).first()
            return user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))