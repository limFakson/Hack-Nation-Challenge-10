-- CreateTable
CREATE TABLE "Talent" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "region" TEXT,
    "availability" TEXT,
    "skills" TEXT,
    "talentScore" INTEGER NOT NULL DEFAULT 0,
    "bio" TEXT,
    "resumeUrl" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "Recruiter" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "companyName" TEXT NOT NULL,
    "contactName" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "Job" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "requiredSkills" TEXT NOT NULL,
    "requiredRegion" TEXT,
    "availabilityRequirement" TEXT,
    "status" TEXT NOT NULL DEFAULT 'Open',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    "recruiterId" INTEGER NOT NULL,
    CONSTRAINT "Job_recruiterId_fkey" FOREIGN KEY ("recruiterId") REFERENCES "Recruiter" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "Assignment" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "talentId" INTEGER NOT NULL,
    "jobId" INTEGER NOT NULL,
    "assignedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "status" TEXT NOT NULL DEFAULT 'Pending',
    CONSTRAINT "Assignment_talentId_fkey" FOREIGN KEY ("talentId") REFERENCES "Talent" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "Assignment_jobId_fkey" FOREIGN KEY ("jobId") REFERENCES "Job" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "PastWork" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "talentId" INTEGER NOT NULL,
    "jobId" INTEGER NOT NULL,
    "completionDate" DATETIME NOT NULL,
    "recruiterFeedback" TEXT NOT NULL,
    "rating" INTEGER NOT NULL,
    "projectComplexityScore" INTEGER NOT NULL,
    CONSTRAINT "PastWork_talentId_fkey" FOREIGN KEY ("talentId") REFERENCES "Talent" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "PastWork_jobId_fkey" FOREIGN KEY ("jobId") REFERENCES "Job" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "Talent_email_key" ON "Talent"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Recruiter_email_key" ON "Recruiter"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Assignment_talentId_jobId_key" ON "Assignment"("talentId", "jobId");
