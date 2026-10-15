from fastapi import FastAPI

from routers.employee_router import router as employee_router
from routers.cookie_router import router as cookie_router 

#set app
app = FastAPI( title="Employee Payroll Management API Demo ", version="1.0.0")

#include the router 
app.include_router(employee_router)
app.include_router(cookie_router)


