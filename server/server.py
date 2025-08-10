from fastapi import Response, FastAPI, HTTPException, Request, Depends, dependencies
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from prisma import Prisma
from dotenv import load_dotenv
import json

from typing import List, Optional
from middleware.JWTAuthMiddleware import JWTAuthMiddleware
from helpers.email_validator import is_valid_email
from helpers.token_generator import create_access_token
from helpers.password_validator import hash_password, verify_password
from schema.db_model import (
    Talent,
    TalentCreate,
    TalentUpdate,
    TalentLoginResponse,
    PastWork,
    Job,
    JobCreate,
    JobAssignmentRequest,
    Recruiter,
    RecruiterCreate,
    RecruiterUpdate,
    RecruiterLoginResponse,
)

load_dotenv()

app = FastAPI()
db = Prisma()

origins = [
    "http://localhost:3000",  # for dev frontend
    "http://127.0.0.1:8000",
    "*",  # <-- allow all (if you're testing, remove in prod!)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(JWTAuthMiddleware)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/talent/login")


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def main():
    message = "Hello welcome to talentAi api"
    return Response({"message": message}, status_code=200)


@app.post("/api/auth/talent/signup", response_model=Talent)
async def registration(talent: TalentCreate):
    hashed_password = hash_password(talent.password)

    if not is_valid_email(talent.email):
        return Response({"error": "Invalid email input"}, status_code=400)

    new_talent = await db.talent.create(
        data={**talent.dict(exclude={"password"}), "password": hashed_password}
    )
    return new_talent


@app.post("/api/auth/talent/login", response_model=TalentLoginResponse)
async def login(email: str, password: str):
    # Find user by email
    talent = await db.talent.find_unique(where={"email": email})
    if not talent:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    if not verify_password(password, talent.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT
    access_token = create_access_token({"id": str(talent.id), "name": talent.name})

    return {"talent": talent, "access_token": access_token, "token_type": "bearer"}


@app.patch("/api/auth/talent/{talent_id}", response_model=TalentUpdate)
async def update_talent_details(
    talent_id: str,
    update_data: TalentUpdate,
    request: Request,
):
    """
    Updates a talent's details.

    The function uses JWT authentication to ensure that only the authenticated
    user can modify their own profile. The talent_id in the URL must match
    the ID from the JWT payload.
    """

    # We get the authenticated user's ID from the request state,
    try:
        user_id_from_token = request.state.user["id"]
    except (AttributeError, KeyError):
        raise HTTPException(
            status_code=403, detail="Not authenticated or invalid token."
        )

    if talent_id != user_id_from_token:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to update this profile.",
        )

    # Create a dictionary of the fields to update, excluding None values
    update_payload = {
        key: value for key, value in update_data.dict().items() if value is not None
    }

    # If the payload is empty, there's nothing to update.
    if not update_payload:
        return {}

    if update_payload.get("skills"):
        update_payload["skills"] = json.dumps(update_payload["skills"])

    # Use the Prisma client to perform the update.
    updated_talent = await db.talent.update(
        where={"id": int(talent_id)}, data=update_payload
    )

    if not updated_talent:
        raise HTTPException(status_code=404, detail="Talent not found.")

    if updated_talent.skills:
        updated_talent.skills = json.loads(updated_talent.skills)

    return updated_talent


# Recruiter Auth Api
@app.post("/api/auth/recruiter/signup", response_model=Recruiter)
async def registration(recruiter: RecruiterCreate):
    hashed_password = hash_password(recruiter.password)

    if not is_valid_email(recruiter.email):
        return Response({"error": "Invalid email input"}, status_code=400)

    new_recruiter = await db.recruiter.create(
        data={**recruiter.dict(exclude={"password"}), "password": hashed_password}
    )
    return new_recruiter


@app.post("/api/auth/recruiter/login", response_model=RecruiterLoginResponse)
async def login(email: str, password: str):
    # Find user by email
    recruiter = await db.recruiter.find_unique(where={"email": email})
    if not recruiter:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    if not verify_password(password, recruiter.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT
    access_token = create_access_token(
        {"id": str(recruiter.id), "name": recruiter.contactName}
    )

    return {"talent": recruiter, "access_token": access_token, "token_type": "Bearer"}


@app.patch("/api/auth/recruiter/{recruiter_id}", response_model=Recruiter)
async def update_recruiter_details(
    recruiter_id: str,
    update_data: RecruiterUpdate,
    request: Request,
):
    """
    Updates a recruiter's details.

    The function uses JWT authentication to ensure that only the authenticated
    recruiter can modify their own profile. The recruiter_id in the URL must match
    the ID from the JWT payload.
    """

    try:
        user_id_from_token = request.state.user["id"]
    except (AttributeError, KeyError):
        raise HTTPException(
            status_code=403, detail="Not authenticated or invalid token."
        )

    # Check if the recruiter_id in the URL matches the authenticated user's ID
    if recruiter_id != user_id_from_token:
        raise HTTPException(
            status_code=403, detail="You are not authorized to update this profile."
        )

    # Create a dictionary of the fields to update, excluding None values
    update_payload = {
        key: value for key, value in update_data.dict().items() if value is not None
    }

    if not update_payload:
        return {}

    # Use the Prisma client to perform the update.
    updated_recruiter = await db.recruiter.update(
        where={"id": int(recruiter_id)}, data=update_payload
    )

    if not updated_recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found.")

    return updated_recruiter


# Talent and Recruiters me fucntions
@app.get("/api/auth/talent/me", response_model=Talent)
async def get_my_details(request: Request):
    """
    Retrieves the details of the authenticated talent.

    The JWTAuthMiddleware ensures that the request is authenticated and
    adds the user's payload to the request state before this function is called.
    """

    # The user payload is guaranteed to be present here because the middleware
    payload = request.state.user

    # Fetch the talent's details from the database using the ID from the token payload.
    talent_details = await db.talent.find_unique(where={"id": int(payload["id"])})

    if not talent_details:
        raise HTTPException(status_code=404, detail="Talent not found.")

    return talent_details


@app.get("/api/auth/recruiter/me", response_model=Recruiter)
async def get_my_details(request: Request):
    """
    Retrieves the details of the authenticated talent.

    The JWTAuthMiddleware ensures that the request is authenticated and
    adds the user's payload to the request state before this function is called.
    """

    # The user payload is guaranteed to be present here because the middleware
    payload = request.state.user

    # Fetch the talent's details from the database using the ID from the token payload.
    recruiter_details = await db.recruiter.find_unique(where={"id": int(payload["id"])})

    if not recruiter_details:
        raise HTTPException(status_code=404, detail="Talent not found.")

    return recruiter_details


# Api function for job base
@app.post("/jobs", response_model=Job, status_code=201)
async def create_job(
    job_data: JobCreate, request: Request
):
    """
    Creates a new job posting. This endpoint is protected and only accessible
    by authenticated recruiters.
    """
    try:
        recruiter_id = request.state.user["id"]
    except (AttributeError, KeyError):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to create a job.",
        )

    # The JobCreate Pydantic model already includes recruiterId, but we
    if job_data.recruiterId != recruiter_id:
        raise HTTPException(
            status_code=403,
            detail="You can only create jobs for your own account.",
        )

    if job_data.get("requiredSkills"):
        job_data["requiredSkills"] = json.dumps(job_data["requiredSkills"])
        
    new_job = await db.job.create(data=job_data.dict())
    return new_job


@app.get("/jobs/{job_id}", response_model=Job)
async def get_job_details(job_id: str):
    """
    Retrieves the details of a specific job by its ID.
    This is a public endpoint.
    """
    job = await db.job.find_unique(where={"id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    
    if job.requiredSkills:
        job.requiredSkills = json.loads(job.requiredSkills)
        
    return job


@app.post("/jobs/{job_id}/assign", response_model=Job)
async def assign_job_to_talent(
    job_id: str,
    assignment_data: JobAssignmentRequest,
    request: Request,
):
    """
    Assigns a job to a specific talent. This endpoint is protected and only
    accessible by the recruiter who created the job. It also creates a
    record in the PastWork table to track the assignment.
    """
    try:
        recruiter_id = request.state.user["id"]
    except (AttributeError, KeyError):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to assign this job.",
        )

    # Verify that the recruiter owns this job
    job = await db.job.find_unique(where={"id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    if job.recruiterId != recruiter_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to assign this job.",
        )

    # Verify the talent exists
    talent = await db.talent.find_unique(where={"id": assignment_data.talentId})
    if not talent:
        raise HTTPException(status_code=404, detail="Talent not found.")

    # Assign the job to the talent
    assignment = await db.assignment.create(
        data={
            "talentId": assignment_data.talentId,
            "jobId": job_id,
            "status": "In Progress",
        }
    )

    # Update the job status to 'Assigned'
    updated_job = await db.job.update(where={"id": job_id}, data={"status": "Assigned"})

    # Create a record in the PastWork table.
    await db.pastwork.create(
        data={
            "talentId": assignment_data.talentId,
            "jobId": job_id,
            "completionDate": None,  # Will be filled later
            "recruiterFeedbackRating": 0,
            "projectComplexityScore": 0,
        }
    )

    if job.requiredSkills:
        job.requiredSkills = json.loads(job.requiredSkills)

    return updated_job
