from dataclasses import dataclass
from decimal import Decimal


@dataclass
class EmployeeModel:

    employee_id: int
    employee_name: str
    employee_basic_salary: Decimal | float | int
    pf: Decimal | float |int 
    da: Decimal |float |int 
    gross_salary: Decimal |float |int


#  this model is simply a Python representation of database data.