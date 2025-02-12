from fastapi import HTTPException, status, UploadFile, Depends
from app.repositories.complaint_repo import ComplaintRepository
from app.utils.file_upload import upload_file_to_gcs
from app.models.schemas.complaint_schemas import ComplaintResponseSchema
from app.config.settings import settings
from google.cloud import storage

class ComplaintService:
    def __init__(self, complaint_repo: ComplaintRepository = Depends()):
        self.complaint_repo = complaint_repo

    async def file_complaint(self, data: dict):
        try:
            image_url = await upload_file_to_gcs(
                data["file"], 
                folder=settings.COMPLAINT_FOLDER_NAME,
                bucket_name=settings.GCP_BUCKET_NAME,
                service_account_json=settings.SERVICE_ACC_JSON
            )
            complaint = await self.complaint_repo.create_complaint({
                "user_id": data["user_id"],
                "order_id": data["complaint_data"].order_id,
                "product_id": data["complaint_data"].product_id,
                "issue": data["complaint_data"].issue,
                "image_url": image_url,
                "status": "open"
            })
            return ComplaintResponseSchema(**complaint)
        except Exception:
            raise HTTPException(status_code=500, detail="Error filing complaint")

    async def get_complaints(self, data: dict):
        try:
            complaints = await self.complaint_repo.get_complaints_by_seller(data)
            return [ComplaintResponseSchema(**complaint) for complaint in complaints]
        except Exception:
            raise HTTPException(status_code=500, detail="Error fetching complaints")
        
    async def get_complaint_by_id(self, data: dict):
        try:
            db_data = await self.complaint_repo.get_complaint_by_id(data)
            if db_data["product"]["seller_id"] != data["user_id"]:
                raise HTTPException(status_code=403, detail="You are not authorized to perform this action.")
            return ComplaintResponseSchema(**db_data["complaint"])
        except Exception:
            raise HTTPException(status_code=500, detail="Error in fetching complaint")