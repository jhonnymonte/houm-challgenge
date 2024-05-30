from sqlalchemy.orm import Session
from app.models import Property
from app.schemas import PropertyUpdate

class PropertyRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_property(self, address: str, location: str, price: float, description: str):
        property = Property(address=address, location=location, price=price, description=description)
        self.session.add(property)
        self.session.commit()
        return property

    def get_property(self, property_id: int):
        return self.session.query(Property).get(property_id)

    def update_property(self, property_id: int, property_update: PropertyUpdate):
        property = self.get_property(property_id)
        if property:
            if property_update.address is not None:
                property.address = property_update.address
            if property_update.location is not None:
                property.location = property_update.location
            if property_update.price is not None:
                property.price = property_update.price
            if property_update.description is not None:
                property.description = property_update.description
            self.session.commit()
            return property
        return None

    def delete_property(self, property_id: int):
        property = self.get_property(property_id)
        if property:
            self.session.delete(property)
            self.session.commit()
            return True
        return False
