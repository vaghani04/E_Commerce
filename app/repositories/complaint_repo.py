from bson import ObjectId
from app.config.database import db_helper
from app.repositories.product_repo import ProductRepo

class ComplaintRepository:
    def __init__(self):
        self.complaint_collection = db_helper.complaints
        self.product_repo = ProductRepo()

    async def create_complaint(self, data: dict):
        complaint_data = {
            "user_id": data["user_id"],
            "order_id": data["order_id"],
            "product_id": data["product_id"],
            "issue": data["issue"],
            "image_url": data["image_url"],
            "status": data["status"]
        }
        result = await self.complaint_collection.insert_one(complaint_data)
        complaint_data["_id"] = result.inserted_id
        return complaint_data

    async def get_complaints_by_seller(self, data: dict):
            try:
                pipeline = [
                    {
                        "$lookup": {
                            "from": "products",
                            "localField": "product_id",
                            "foreignField": "_id",
                            "as": "product"
                        }
                    },
                    {"$unwind": "$product"},
                    {"$match": {"product.seller_id": data["user_id"]}},
                    {
                        "$project": {
                            "user_id": 1,
                            "order_id": 1,
                            "product_id": 1,
                            "issue": 1,
                            "image_url": 1,
                            "status": 1,
                            "_id": 0
                        }
                    }
                ]
                return await self.complaint_collection.aggregate(pipeline).to_list(None)
            except Exception as e:
                raise Exception(f"Error fetching complaints: {str(e)}")
            

    async def get_complaint_by_id(self, data: dict):
        complaint = await self.complaint_collection.find_one({"_id": ObjectId(data["complaint_id"])})
        product = await self.product_repo.get_product(complaint["product_id"])
        return {"complaint": complaint, "product": product}