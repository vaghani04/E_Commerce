from app.services.complaint_service import ComplaintService
from fastapi import Depends

class GetComplaintsUsecase:
    def __init__(self, complaint_service: ComplaintService = Depends()):
        self.complaint_service = complaint_service

    async def get_complaints(self, data: dict):
        return await self.complaint_service.get_complaints(data)
    
    async def get_complaint_by_id(self, data: dict):
        return await self.complaint_service.get_complaint_by_id(data)
