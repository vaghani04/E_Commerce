from datetime import datetime, timezone
from bson import ObjectId

class Product:
    def __init__(self, title, description, category, price, rating, brand):
        self._id = ObjectId()
        self.title = title
        self.description = description
        self.category = category
        self.price = price
        self.rating = rating
        self.brand = brand
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "_id": str(self._id),
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "rating": self.rating,
            "brand": self.brand,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
