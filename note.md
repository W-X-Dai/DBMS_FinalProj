# notes

- from terminal connect to psql
sudo -u postgres psql

- At psql cli:
list dbs: \l
connect to db: \c <db_name>
list tables: \dt
call system command: \! <command>(eg. \! clear)

- create dbs

```
-- 1. DEPARTMENT
CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(50) UNIQUE NOT NULL,
    supplier_id VARCHAR(10) UNIQUE,
    CONSTRAINT fk_department_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES resource_supplier(supplier_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 2. RESOURCE_SUPPLIER
CREATE TABLE resource_supplier (
    supplier_id VARCHAR(10) PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    role CHAR(1) CHECK (role IN ('A', 'D', 'C')), -- Admin / Department / Company
    supplier_name VARCHAR(50) NOT NULL,
    contact_person VARCHAR(30) NOT NULL,
    email VARCHAR(50) UNIQUE,
    verified_status BOOLEAN DEFAULT FALSE
);

-- 3. STUDENT
CREATE TABLE student (
    student_id VARCHAR(10) PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    student_name VARCHAR(30) NOT NULL,
    department_id INT REFERENCES department(department_id)
        ON DELETE SET DEFAULT ON UPDATE CASCADE,
    email VARCHAR(50) UNIQUE NOT NULL
);

-- 4. STUDENT_GPA
CREATE TABLE student_gpa (
    student_id VARCHAR(10) REFERENCES student(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    semester VARCHAR(10) NOT NULL,
    gpa FLOAT CHECK (gpa BETWEEN 0 AND 4.3),
    PRIMARY KEY (student_id, semester)
);

-- 5. STUDENT_COURSE_RECORD
CREATE TABLE student_course_record (
    student_id VARCHAR(10) REFERENCES student(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    semester VARCHAR(10) NOT NULL,
    course_id VARCHAR(10) NOT NULL,
    score FLOAT CHECK (score BETWEEN 0 AND 100),
    PRIMARY KEY (student_id, semester, course_id)
);

-- 6. ACHIEVEMENT
CREATE TABLE achievement (
    achievement_id SERIAL PRIMARY KEY,
    student_id VARCHAR(10) REFERENCES student(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    category CHAR(1) CHECK (category IN ('C','R','O')), -- Competition, Research, Others
    title VARCHAR(100) NOT NULL,
    description TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status INT CHECK (status IN (0,1,2)) DEFAULT 0 -- 0=unrecognized,1=recognized,2=rejected
);

-- 7. RESOURCE
CREATE TABLE resource (
    resource_id SERIAL PRIMARY KEY,
    resource_type CHAR(1) CHECK (resource_type IN ('S','I','L','O')), -- Scholarship, Intern, Lab, Others
    quota INT CHECK (quota >= 0),
    supplier_id VARCHAR(10) REFERENCES resource_supplier(supplier_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    title VARCHAR(100) NOT NULL,
    deadline DATE NOT NULL,
    description TEXT,
    contact_person VARCHAR(30),
    email VARCHAR(50),
    status INT CHECK (status IN (0,1,2)) DEFAULT 2 -- 0=cancel,1=unavailable,2=available
);

-- 8. RESOURCE_CONDITION
CREATE TABLE resource_condition (
    resource_id INT REFERENCES resource(resource_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    department_id INT REFERENCES department(department_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    avg_gpa FLOAT CHECK (avg_gpa BETWEEN 0 AND 4.3),
    current_gpa FLOAT CHECK (current_gpa BETWEEN 0 AND 4.3),
    is_poor BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (resource_id, department_id)
);

-- 9. APPLICATION
CREATE TABLE application (
    student_id VARCHAR(10) REFERENCES student(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    resource_id INT REFERENCES resource(resource_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    apply_date DATE DEFAULT CURRENT_DATE,
    status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (student_id, resource_id)
);

-- 10. PUSH_RECORD
CREATE TABLE push_record (
    push_id SERIAL PRIMARY KEY,
    pusher_id VARCHAR(10) REFERENCES resource_supplier(supplier_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    student_id VARCHAR(10) REFERENCES student(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    resource_id INT REFERENCES resource(resource_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    push_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```

- test data
```
INSERT INTO resource_supplier VALUES ('C001','testC001','C','TW_Microsoft','Dave Wang','hr@microsoft.com',TRUE);
INSERT INTO department (department_name) VALUES ('DBME');
INSERT INTO student VALUES ('B12508026','test1234','Josh',1,'b12508026@ntu.edu.tw');
INSERT INTO resource (resource_type,quota,supplier_id,title,deadline,description)
VALUES ('I',5,'C001','AI intern','2025-12-31','An intenrnship position at Microsoft for AI research.');
```