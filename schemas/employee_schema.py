from pydantic import BaseModel , Field , field_validator , ConfigDict,model_validator

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

#partial update - send only the fields you want to change
class PatchEmployee(BaseModel):

    model_config = ConfigDict(extra='forbid')

    EmployeeName : str | None = Field(default=None, min_length=3, max_length=100, pattern=r"^[A-Za-z ]+$")
    EmployeeBasicSalary : float | None = Field(default=None, **BASIC_SALARY)

    @field_validator("EmployeeName")
    @classmethod
    def name_validator(cls,name):
        if name is not None and not name.strip():
            raise ValueError("Fill the employee name")
        return name

    @model_validator(mode="after")
    def check_fields_sent(self):
        if not self.model_fields_set:
            raise ValueError("Send at least one field to update")

        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")

        return self