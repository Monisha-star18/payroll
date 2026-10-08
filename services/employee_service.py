from repositories.employee_repository import (
    fetch_all_employees , 
    post_new_employee , 
    delete_employee  , 
    put_employee,
    fetch_employee_by_id)

from .payroll_service import PayrollService

from fastapi import HTTPException


#get employee deatiles
async def get_all_employees() :

    columns ,employees_data  = await fetch_all_employees()

    employees = []

    for employee in employees_data :

        employee_data = dict(zip(columns,employee))
        employees.append(employee_data)

    return employees

#create new employee and post 
async def create_employee(employee_data):

    employee_details = employee_data.model_dump()

    basic_salary=employee_details['EmployeeBasicSalary']

    da = PayrollService.calculate_da(basic_salary)
    pf = PayrollService.calculate_pf(basic_salary)
    gross_salary = PayrollService.calculate_gross_salary(basic_salary)


    salary_deatils = { "DA": da,
                        "PF": pf,
                        "GrossSalary": gross_salary}

    employee = {
        **employee_details,
        **salary_deatils
    }

    return await post_new_employee(employee)

#update the employee
async def update_employee(employee_data,employee_id):

    employee_details = employee_data.model_dump()
    
    basic_salary=employee_details['EmployeeBasicSalary']
    
    da = PayrollService.calculate_da(basic_salary)
    pf = PayrollService.calculate_pf(basic_salary)
    gross_salary = PayrollService.calculate_gross_salary(basic_salary)
    
        
    salary_deatils = { "DA": da,
                    "PF": pf,
                    "GrossSalary": gross_salary}
    
    employee = {
            **employee_details,
            **salary_deatils
        }

    return await put_employee(employee,employee_id)


#delete the employee detail 
async def remove_employee_byid(employee_id):

    return await delete_employee(employee_id)

#get by id 
async def get_employee_byid(employee_id):

    columns, employee_data = await fetch_employee_by_id(employee_id)

    if employee_data is None:
        raise HTTPException(
            status_code=404,
            detail=f"Employee with ID {employee_id} not found"
        )

    return dict(zip(columns, employee_data))