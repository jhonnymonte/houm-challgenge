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

    def update_employee(self, employee_id: int, employee: EmployeeUpdate):
        db_employee = self.session.query(Employee).filter(Employee.id == employee_id).first()
        if not db_employee:
            return None

        for var, value in vars(employee).items():
            if value is not None:  # Update only if value is not None
                setattr(db_employee, var, value)

        self.session.commit()
        self.session.refresh(db_employee)
        return db_employee

    def delete_employee(self, employee_id: int):
        db_employee = self.session.query(Employee).filter(Employee.id == employee_id).first()
        if db_employee is None:
            return None
        self.session.delete(db_employee)
        self.session.commit()
        return db_employee


def get_employee_repository(session: Session) -> EmployeeRepository:
    return EmployeeRepository(session)
