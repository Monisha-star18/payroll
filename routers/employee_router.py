from fastapi import APIRouter,Path,Query

from schemas.employee_schema import (CreateEmployee , UpdateEmployee,PatchEmployee)

from services.employee_service import (
                        get_all_employees , 
                        create_employee ,
                        remove_employee_byid,
                        update_employee,
                        get_employee_byid,
                        partial_update_employee) 


router = APIRouter( prefix="/api/employees")


#get employees and salary deatils
@router.get("/")
async def get_employees( page:int = Query(1,ge=1),
                         page_size:int = Query(10,ge=1,le=100) ):
    
    return await get_all_employees(page,page_size)



#post the detailes 
@router.post("/")
async def create_new_employee(employee_data : CreateEmployee):

    return await create_employee(employee_data)

#update the whole employee 
@router.put('/{employee_id}')
async def update_employee_detailes( 
    employee_data :UpdateEmployee,
    employee_id:int =Path(gt=0)
    ):

    return await update_employee(employee_data,employee_id)


#delect an employee
@router.delete('/{employee_id}')
async def remove_employee(employee_id : int =Path(gt=0) ):

    return await remove_employee_byid(employee_id)


#get one employee by id
@router.get("/{employee_id}")
async def get_employee(employee_id: int = Path(gt=0)):

    return await get_employee_byid(employee_id)

#update only the given fields of an employee
@router.patch('/{employee_id}')
async def patch_employee_detailes(
    employee_data : PatchEmployee,
    employee_id : int =Path(gt=0)
    ):

    return await partial_update_employee(employee_data,employee_id)