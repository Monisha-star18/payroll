
CREATE DATABASE payroll_db;

CREATE TABLE employees (
    employee_id            INTEGER        PRIMARY KEY CHECK (employee_id > 0),
    employee_name          VARCHAR(100)   NOT NULL,
    employee_basic_salary  NUMERIC(12,2)  NOT NULL CHECK (employee_basic_salary >= 5000),
    pf                     NUMERIC(12,2)  NOT NULL,
    da                     NUMERIC(12,2)  NOT NULL,
    gross_salary           NUMERIC(12,2)  NOT NULL
);