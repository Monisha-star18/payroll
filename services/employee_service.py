from repositories.employee_repository import EmployeeRepository
from repositories import file_repository

from .payroll_service import PayrollService

from fastapi import HTTPException, UploadFile

class EmployeeService:

    def __init__(self):
        self.payroll_services = PayrollService()
        self.employee_repository = EmployeeRepository()
        
    #get employee deatiles
    async def get_all_employees(self,page:int , page_size:int) :

        offset = (page -1 ) * page_size

        employees_data  = await self.employee_repository.fetch_all_employees(page_size , offset)

        return { "data" : employees_data ,
                "page": page,
                "page_size": page_size,
                }

    #create new employee and post 
    async def create_employee(self,employee_data):

        employee_details = employee_data.model_dump()

        basic_salary=employee_details['EmployeeBasicSalary']

        da = self.payroll_services.calculate_da(basic_salary)
        pf = self.payroll_services.calculate_pf(basic_salary)
        gross_salary = self.payroll_services.calculate_gross_salary(basic_salary)


        salary_deatils = { "DA": da,
                            "PF": pf,
                            "GrossSalary": gross_salary}

        employee = {
            **employee_details,
            **salary_deatils
        }

        return await self.employee_repository.post_new_employee(employee)

    #update the employee
    async def update_employee(self,employee_data,employee_id):

        employee_details = employee_data.model_dump()
        
        basic_salary=employee_details['EmployeeBasicSalary']
        
        da = self.payroll_services.calculate_da(basic_salary)
        pf = self.payroll_services.calculate_pf(basic_salary)
        gross_salary = self.payroll_services.calculate_gross_salary(basic_salary)
        
            
        salary_deatils = { "DA": da,
                        "PF": pf,
                        "GrossSalary": gross_salary}
        
        employee = {
                **employee_details,
                **salary_deatils
            }

        return await self.employee_repository.put_employee(employee,employee_id)


    #delete the employee detail 
    async def remove_employee_byid(self,employee_id):

        return await self.employee_repository.delete_employee(employee_id)

    #get by id 
    async def get_employee_byid(self,employee_id):

        employee_data = await self.employee_repository.fetch_employee_by_id(employee_id)

        if employee_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with ID {employee_id} not found"
            )

        return  employee_data

    #partially update the employee
    async def partial_update_employee(self,employee_data,employee_id):


        changes = employee_data.model_dump(exclude_unset=True)

        if "EmployeeBasicSalary" in changes:

            basic_salary = changes["EmployeeBasicSalary"]

            changes["DA"] = PayrollService.calculate_da(basic_salary)
            changes["PF"] = PayrollService.calculate_pf(basic_salary)
            changes["GrossSalary"] = PayrollService.calculate_gross_salary(basic_salary)

        columns, updated_employee = await self.employee_repository.patch_employee(changes,employee_id)

        if updated_employee is None:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with ID {employee_id} not found"
            )

        return {
            "message" : "Updated Successfully",
            "EmployeeID" : employee_id,
            "Employee" : dict(zip(columns, updated_employee))
        }

    #upload the resume (pdf) of an employee
    async def upload_employee_resume(self, employee_id, file: UploadFile):

        employee = await self.employee_repository.fetch_employee_by_id(employee_id)

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with ID {employee_id} not found"
            )

        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )

        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Invalid file content type"
            )

        file_path = await file_repository.save_file(file)

        await self.employee_repository.save_resume_path(employee_id, file_path)

        return {
            "message": "Resume uploaded successfully",
            "EmployeeID": employee_id,
            "file_path": file_path
        }

employee_service = EmployeeService()