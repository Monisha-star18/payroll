from database.connection import get_connection
from exceptions.employee_exceptions import EmployeeRepositoryError
from psycopg.errors import UniqueViolation
from fastapi import HTTPException

#get all employee
async def fetch_all_employees():

    try:
        connection = await get_connection()

        async with connection:
            async with connection.cursor() as cursor :  #creating the cursor to write the sql 

                query = """ SELECT * FROM employees """

                await cursor.execute (query) #Send SQL command to database

                columns = [column.name for column in cursor.description] # get all the column names using description 

                employees_data = await cursor.fetchall() #Gets all rows returned by the query

                return columns , employees_data 
            
    except Exception as er :
        raise EmployeeRepositoryError( f"Iusse in repositry : {er}")
    
#create new employees
async def post_new_employee(employee):
    try:
        connection = await get_connection()
        
        async with connection:
            async with connection.cursor() as cursor :  

                query = """ INSERT INTO employees ( 
                            employee_id,
                            employee_name,
                            employee_basic_salary,
                            pf,
                            da,
                            gross_salary) VALUES (%s, %s, %s, %s, %s, %s)  """
                
                values = ( employee["EmployeeId"], employee["EmployeeName"],
                           employee["EmployeeBasicSalary"], employee["PF"],
                           employee["DA"], employee["GrossSalary"])

                await cursor.execute(query,values)

                await connection.commit()

                return {
                        "message":"Employee Created",
                        "EmployeeId" :employee["EmployeeId"] ,
                        "EmployeeName" : employee["EmployeeName"]
                        }


    except UniqueViolation:
        raise HTTPException( 
             status_code=409, 
             detail=f"Employee with ID {employee['EmployeeId']} already exists")
            

#update employees
async def put_employee(employee_data,employee_id):
    try:
        connection = await get_connection()

        async with connection:
            async with connection.cursor() as cursor:

                query = """ UPDATE employees 
                            SET 
                            employee_name =%s,
                            employee_basic_salary=%s,
                            pf = %s,
                            da = %s,
                            gross_salary =%s
                            
                            WHERE employee_id =%s
                            
                            RETURNING employee_id, employee_name, employee_basic_salary, pf,da,gross_salary 
                        """
                
                values = (employee_data["EmployeeName"],employee_data["EmployeeBasicSalary"],
                         employee_data["PF"],employee_data["DA"], employee_data["GrossSalary"],employee_id )

                await cursor.execute(query,values)

                updated_employee_detail =await cursor.fetchone()

                if updated_employee_detail is None:
                     return {"message" :f"Employee with the id {employee_id} is not found "}

                await connection.commit()

                return {"message" : "Updated Successfully","EmployeeID" : employee_id}
                     
                        

    except Exception as er:
                raise EmployeeRepositoryError( f"Iusse in repositry : {er}")


#delete employees 

async def delete_employee(employee_id):
    try:
        connection = await get_connection()
        
        async with connection:
            async with connection.cursor() as cursor :

                query=""" DELETE FROM employees WHERE employee_id = %s"""

                await cursor.execute(query,(employee_id,))
                

                if cursor.rowcount == 0:
                    return {
                        "message": "Employee not found",
                        "employee_id": employee_id
                    }

                await connection.commit()

                return {
                    "message": "Employee deleted successfully",
                    "employee_id": employee_id
                }
                
    except Exception as er:
            raise EmployeeRepositoryError( f"Iusse in repositry : {er}")

#get by id 
async def fetch_employee_by_id(employee_id):

    try:
        connection = await get_connection()

        async with connection:
            async with connection.cursor() as cursor:

                query = """ SELECT * FROM employees WHERE employee_id = %s """

                await cursor.execute(query, (employee_id,))
                
                columns = [column.name for column in cursor.description]

                employee_data = await cursor.fetchone()  # one row, or None

                return  columns, employee_data

    except Exception as er:
        raise EmployeeRepositoryError(f"Iusse in repositry : {er}")