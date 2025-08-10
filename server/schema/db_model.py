from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


# A Pydantic BaseConfig with orm_mode = True is crucial.
# It tells Pydantic to read data from an ORM object (like Prisma's generated models)
# even if it's not a dictionary. This is how you can directly pass a Prisma model
# to a Pydantic model for validation and serialization.
class Config:
    orm_mode = True


# Schemas for Talents
class TalentBase(BaseModel):
    email: str
    name: str
    region: Optional[str] = None
    availability: Optional[str] = None
    skills: Optional[str] = None
    talentScore: int = None
    bio: Optional[str] = None
    resumeUrl: Optional[str] = None


class TalentCreate(TalentBase):
    password: str


class Talent(TalentBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config(Config):
        pass


class TalentUpdate(BaseModel):
    name: Optional[str] = None
    region: Optional[str] = None
    availability: Optional[str] = None
    skills: Optional[List[str]] = None
    bio: Optional[str] = None
    resumeUrl: Optional[str] = None

    class Config(Config):
        pass


class TalentLoginResponse(BaseModel):
    talent: TalentBase
    access_token: str
    token_type: str = "bearer"


# Schemas for Recruiters
class RecruiterBase(BaseModel):
    email: str
    companyName: str
    contactName: str


class RecruiterCreate(RecruiterBase):
    password: str


class Recruiter(RecruiterBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config(Config):
        pass


class RecruiterLoginResponse(BaseModel):
    talent: RecruiterBase
    access_token: str
    token_type: str = "bearer"


class RecruiterUpdate(BaseModel):
    companyName: Optional[str] = None
    contactName: Optional[str] = None

    class Config(Config):
        pass


# Schemas for Jobs
class JobBase(BaseModel):
    title: str
    description: str
    requiredSkills: List[str]
    requiredRegion: Optional[str] = None
    availabilityRequirement: Optional[str] = None


class JobCreate(JobBase):
    recruiterId: str


class Job(JobBase):
    id: int
    status: str
    createdAt: datetime
    updatedAt: datetime

    class Config(Config):
        pass


# Schemas for Assignments
class AssignmentBase(BaseModel):
    talentId: str
    jobId: str


class Assignment(AssignmentBase):
    id: int
    assignedAt: datetime
    status: str

    class Config(Config):
        pass


# Schemas for PastWork
class PastWorkBase(BaseModel):
    talentId: str
    jobId: str
    completionDate: datetime
    recruiterFeedback: str
    rating: int
    projectComplexityScore: int


class PastWork(PastWorkBase):
    id: int

    class Config(Config):
        pass
