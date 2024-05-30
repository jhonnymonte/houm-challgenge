from sqlalchemy.orm import Session
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate
from sqlalchemy import func

class EmployeeRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_employee(self, name: str, email: str, password: str):
        employee = Employee(name=name, email=email, hashed_password=password)
        self.session.add(employee)
        self.session.commit()
        return employee

    def get_employee(self, employee_id: int):
        return self.session.query(Employee).get(employee_id)
    
    def get_employee_by_email(self, email: str):
        return self.session.query(Employee).filter(func.lower(Employee.email) == func.lower(email)).first()

    def update_employee(self, employee_id: int, name: str, email: str):
        employee = self.get_employee(employee_id)
        if employee:
            employee.name = name
            employee.email = email
            self.session.commit()
            return True
        return False

    def delete_employee(self, employee_id: int):
        employee = self.get_employee(employee_id)
        if employee:
            self.session.delete(employee)
            self.session.commit()
            return True
        return False

def get_employee_repository(session: Session) -> EmployeeRepository:
    return EmployeeRepository(session)
