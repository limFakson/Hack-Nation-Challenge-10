TalentAI Backend
================

An AI-powered marketplace built to revolutionize the hiring process for AI and technical talent. This backend service provides the core functionality for talent and recruiter management, job postings, and a sophisticated AI-driven matching and grading system.

### **Key Features**

*   **AI-Powered Talent Grading:** A multi-factor grading system evaluates talents based on their resume, skills, availability, region, and past performance on the platform.
    
*   **Intelligent Job Matching:** The system matches jobs with the best-fit candidates, using a conditional round-robin selection technique to ensure fair distribution and consider factors like recent job assignments.
    
*   **Secure Authentication:** A **JWT-based authentication** system protects all user-specific endpoints, ensuring that users can only access and modify their own data.
    
*   **Scalable Database:** The backend uses **FastAPI** and a **PostgreSQL** database, managed with **Prisma**, to ensure the system can handle a large volume of data and users efficiently.
    

### **Tech Stack**

*   **Backend Framework:** FastAPI
    
*   **Programming Language:** Python
    
*   **Database:** PostgreSQL
    
*   **ORM:** Prisma with prisma-client-py
    
*   **Password Hashing:** passlib\[bcrypt\]
    
*   **Authentication:** PyJWT
    

### **API Endpoints**

#### **Talent Endpoints**

*   POST /talent/signup: Registers a new talent.
    
*   POST /talent/login: Logs in a talent and returns a JWT token.
    
*   GET /api/auth/talent/me: Retrieves the details of the authenticated talent.
    
*   PATCH /api/auth/talent/{talent_id}: Updates the details of the authenticated talent's profile.
    

#### **Recruiter Endpoints**

*   POST /api/auth/recruiter/signup: Registers a new recruiter.
    
*   POST /api/auth/recruiter/login: Logs in a recruiter and returns a JWT token.
    
*   GET /api/auth/recruiter/me: Retrieves the details of the authenticated recruiter.
    
*   PATCH /api/auth/recruiter/{recruiter_id}: Updates the details of the authenticated recruiter's profile.
    

#### **Other Endpoints** (not done yet)

*   POST /jobs: Creates a new job posting (**Recruiter only**).
    
*   GET /jobs/{job_id}/candidates: Finds the best candidates for a specific job (**Recruiter only**).

## Every endpoints needs an authorization token header excluding /login, /signup, /docs, /open.json
    

### **What We Have Done So Far**

The project's foundational work is complete. We've defined the database schema with Prisma, set up the FastAPI framework, and implemented crucial functionalities, including:

*   Pydantic models for data validation and serialization.
    
*   A secure **JWT token** creation and validation system with middleware.
    
*   A password hashing utility using passlib\[bcrypt\].
    
*   API functions for **user registration, login, and profile updates** for both talents and recruiters.
    

We are now ready to build out the core job matching and talent grading logic.