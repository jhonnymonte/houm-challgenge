from sqlalchemy.orm import Session
from app.models import PropertyVisit
from app.schemas import PropertyVisitCreate
from datetime import datetime

class PropertyVisitRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_property_visit(self, property_id: int, visit_date: datetime, visitor_name: str, visitor_email: str, employee_id: int = None, feedback: str = None):
        property_visit = PropertyVisit(
            property_id=property_id,
            visit_date=visit_date,
            visitor_name=visitor_name,
            visitor_email=visitor_email,
            employee_id=employee_id,
            feedback=feedback
        )
        self.session.add(property_visit)
        self.session.commit()
        return property_visit

    def get_property_visit(self, visit_id: int):
        return self.session.query(PropertyVisit).get(visit_id)

    def update_property_visit(self, visit_id: int, property_visit_update: PropertyVisitCreate):
        property_visit = self.get_property_visit(visit_id)
        if property_visit:
            if property_visit_update.property_id is not None:
                property_visit.property_id = property_visit_update.property_id
            if property_visit_update.visit_date is not None:
                property_visit.visit_date = property_visit_update.visit_date
            if property_visit_update.visitor_name is not None:
                property_visit.visitor_name = property_visit_update.visitor_name
            if property_visit_update.visitor_email is not None:
                property_visit.visitor_email = property_visit_update.visitor_email
            self.session.commit()
            return property_visit
        return None

    def delete_property_visit(self, visit_id: int):
        property_visit = self.get_property_visit(visit_id)
        if property_visit:
            self.session.delete(property_visit)
            self.session.commit()
            return True
        return False
