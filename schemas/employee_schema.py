from pydantic import BaseModel , Field , field_validator , ConfigDict

NAME = dict(min_length=3, max_length=100,default="",pattern=r"^[A-Za-z ]+$")
BASIC_SALARY = dict(ge=5_000,lt=1_000_000)

class CreateEmployee(BaseModel) :

    model_config = ConfigDict(extra='forbid')

    EmployeeId   : int = Field(gt=0)
    EmployeeName : str = Field(**NAME)
    EmployeeBasicSalary : float = Field(**BASIC_SALARY)

    @field_validator("EmployeeName")
    @classmethod
    def name_validator(cls,name):
        if not name:
            raise ValueError("Fill the employee name")
        return name

class UpdateEmployee(BaseModel):
    
    model_config = ConfigDict(extra='forbid')

    EmployeeName : str = Field(**NAME)
    EmployeeBasicSalary : float = Field(**BASIC_SALARY)

    @field_validator("EmployeeName")
    @classmethod
    def name_validator(cls,name):
        if not name:
            raise ValueError("Fill the employee name")
        return name

    

