-- Resume Table
CREATE TABLE IF NOT EXISTS resumes (
    resume_id SERIAL PRIMARY KEY,
    file_name VARCHAR(255),
    parsed_text TEXT,
    target_role VARCHAR(100),
    experience_level VARCHAR(50),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Extracted Skills Table
CREATE TABLE IF NOT EXISTS extracted_skills (
    skill_id SERIAL PRIMARY KEY,
    resume_id INT REFERENCES resumes(resume_id),
    skill_name VARCHAR(100),
    confidence_score FLOAT
);

-- Job Roles Table
CREATE TABLE IF NOT EXISTS job_roles (
    job_id SERIAL PRIMARY KEY,
    role_name VARCHAR(100),
    required_skills TEXT,
    salary_range VARCHAR(100),
    location VARCHAR(100),
    experience_required VARCHAR(50)
);

-- Skill Gap Analysis Table
CREATE TABLE IF NOT EXISTS skill_gap_analysis (
    analysis_id SERIAL PRIMARY KEY,
    resume_id INT REFERENCES resumes(resume_id),
    matched_skills TEXT,
    missing_skills TEXT,
    gap_score FLOAT,
    recommendation TEXT
);