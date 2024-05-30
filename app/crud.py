from sqlalchemy.orm import Session
from app.repositories.employee import EmployeeRepository
from app.repositories.property import PropertyRepository
from app.repositories.property_visit import PropertyVisitRepository
from app.schemas import EmployeeCreate, EmployeeUpdate, PropertyCreate,PropertyVisitCreate,PropertyVisitUpdate,PropertyUpdate,PropertyVisit



def get_employee_repository(db: Session) -> EmployeeRepository:
    return EmployeeRepository(session=db)

def get_property_repository(db: Session) -> PropertyRepository:
    return PropertyRepository(db)

def get_property_visit_repository(db: Session) -> PropertyVisitRepository:
    return PropertyVisitRepository(db)

# Funciones CRUD para Employee
def get_employee(db: Session, employee_id: int):
    return get_employee_repository(db).get_employee(employee_id)

def get_employee_by_email(db: Session, email: str):
    return get_employee_repository(db).get_employee_by_email(email)

def create_employee(db: Session, employee: EmployeeCreate):
    return get_employee_repository(db).create_employee(employee)

def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    return get_employee_repository(db).update_employee(employee_id, employee)

def delete_employee(db: Session, employee_id: int):
    return get_employee_repository(db).delete_employee(employee_id)

#funciones Crud para proyperty

def create_property(db: Session, property: PropertyCreate):
    return get_property_repository(db).create_property(property)


def get_property(db: Session, property_id: int):
    return get_property_repository(db).get_property(property_id)

def update_property(db: Session, property_id: int, property: PropertyUpdate):
    return get_property_repository(db).update_property(property_id, property)

def delete_property(db: Session, property_id: int):
    return get_property_repository(db).delete_property(property_id)

#funciones crud para vistis
def create_property_visit(db: Session, property_visit: PropertyVisitCreate):
    return get_property_visit_repository(db).create_property_visit(property_visit)

def get_property_visit(db: Session, visit_id: int):
    return get_property_visit_repository(db).get_property_visit(visit_id)

def update_property_visit(db: Session, visit_id: int, property_visit: PropertyVisitUpdate):
    return get_property_visit_repository(db).update_property_visit(visit_id, property_visit)

def delete_property_visit(db: Session, visit_id: int):
    return get_property_visit_repository(db).delete_property_visit(visit_id)

def get_visits_by_employee(db: Session, employee_id: int):
    return db.query(PropertyVisit).filter(PropertyVisit.employee_id == employee_id).all()