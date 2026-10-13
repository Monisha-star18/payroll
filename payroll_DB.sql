
CREATE DATABASE payroll_db;

CREATE TABLE employees (
    employee_id            INTEGER        PRIMARY KEY CHECK (employee_id > 0),
    employee_name          VARCHAR(100)   NOT NULL,
    employee_basic_salary  NUMERIC(12,2)  NOT NULL CHECK (employee_basic_salary >= 5000),
    pf                     NUMERIC(12,2)  NOT NULL,
    da                     NUMERIC(12,2)  NOT NULL,
    gross_salary           NUMERIC(12,2)  NOT NULL
);

-- relationship : one employee -> one resume
-- employee_id is both the primary key and the link to employees
-- (deleting the employee also deletes the resume row)
CREATE TABLE employee_resumes (
    employee_id  INTEGER       PRIMARY KEY,
    resume_path  VARCHAR(255)  NOT NULL,

    CONSTRAINT fk_employee_resume
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
        ON DELETE CASCADE
);
