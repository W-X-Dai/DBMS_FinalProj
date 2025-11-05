CREATE DATABASE group_7;
\c group_7;

-- UUID 
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-------------------------------------------------
-- Core user
-------------------------------------------------
CREATE TABLE "user" (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    real_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    role VARCHAR(20) CHECK(role IN ('student','department','company')),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

-------------------------------------------------
-- Profile tables
-------------------------------------------------
CREATE TABLE department_profile (
    department_id UUID PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    contact_person UUID NOT NULL REFERENCES "user"(user_id) -- who manages this department
);

CREATE TABLE student_profile (
    user_id UUID PRIMARY KEY REFERENCES "user"(user_id), -- 1:1
    student_id VARCHAR(10) UNIQUE NOT NULL,
    department_id UUID NOT NULL REFERENCES department_profile(department_id),
    entry_year INT NOT NULL,
    grade INT NOT NULL
);

CREATE TABLE company_profile (
    company_id UUID PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    contact_person UUID NOT NULL REFERENCES "user"(user_id), -- who manages this company
    industry VARCHAR(50) NOT NULL
);

-------------------------------------------------
-- Student affiliation 
-------------------------------------------------
CREATE TABLE student_department (
    user_id UUID REFERENCES "user"(user_id),
    department_id UUID NOT NULL REFERENCES department_profile(department_id),
    role VARCHAR(20) CHECK(role IN ('major','minor','double_major')),
    start_semester VARCHAR(10) NOT NULL,
    end_semester VARCHAR(10),
    PRIMARY KEY(user_id, department_id, role, start_semester)
);

-------------------------------------------------
-- History: GPA / Courses
-------------------------------------------------
CREATE TABLE student_gpa (
    user_id UUID REFERENCES "user"(user_id),
    semester VARCHAR(10) NOT NULL,
    gpa FLOAT CHECK(gpa BETWEEN 0 AND 4.3),
    PRIMARY KEY(user_id, semester)
);

CREATE TABLE student_course_record (
    user_id UUID REFERENCES "user"(user_id),
    semester VARCHAR(10) NOT NULL,
    course_id VARCHAR(50) NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    score FLOAT CHECK(score BETWEEN 0 AND 100),
    PRIMARY KEY(user_id, semester, course_id)
);

-------------------------------------------------
-- Achievement
-------------------------------------------------
CREATE TABLE achievement (
    achievement_id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES "user"(user_id),
    category VARCHAR(20) CHECK(category IN ('Competition','Research','Others')),
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK(status IN ('unrecognized','recognized','rejected')) NOT NULL
);

-------------------------------------------------
-- Resource 
-------------------------------------------------
CREATE TABLE resource (
    resource_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    resource_type VARCHAR(20) CHECK(resource_type IN ('Scholarship','Internship','Lab','Others')),
    quota INT NOT NULL CHECK(quota >= 0),
    
    department_supplier_id UUID REFERENCES department_profile(department_id),
    company_supplier_id UUID REFERENCES company_profile(company_id),
    
    -- XOR check: make sure that only one of the two supplier IDs is NOT NULL
    CHECK (
        (department_supplier_id IS NOT NULL AND company_supplier_id IS NULL) OR 
        (department_supplier_id IS NULL AND company_supplier_id IS NOT NULL)
    ),
    
    title VARCHAR(100) NOT NULL,
    deadline DATE,
    description TEXT NOT NULL,
    status VARCHAR(20) CHECK(status IN ('Canceled','Unavailable','Available')) NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE
);

-------------------------------------------------
-- Eligibility rule
-------------------------------------------------
CREATE TABLE resource_condition (
    resource_id UUID REFERENCES resource(resource_id),
    department_id UUID NOT NULL REFERENCES department_profile(department_id),
    avg_gpa FLOAT CHECK(avg_gpa BETWEEN 0 AND 4.3), -- NULL means no limit
    current_gpa FLOAT CHECK(current_gpa BETWEEN 0 AND 4.3), -- NULL means no limit
    is_poor BOOLEAN,
    PRIMARY KEY(resource_id, department_id)
);

-------------------------------------------------
-- Application
-------------------------------------------------
CREATE TABLE application (
    user_id UUID REFERENCES "user"(user_id),
    resource_id UUID REFERENCES resource(resource_id),
    apply_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) CHECK(status IN ('submitted','under_review','approved','rejected')) NOT NULL,
    PRIMARY KEY(user_id, resource_id)
);

-------------------------------------------------
-- Push notification 
-------------------------------------------------
CREATE TABLE push_record (
    push_id SERIAL PRIMARY KEY,
    pusher_id UUID REFERENCES "user"(user_id),
    receiver_id UUID REFERENCES "user"(user_id),
    resource_id UUID REFERENCES resource(resource_id),
    push_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
