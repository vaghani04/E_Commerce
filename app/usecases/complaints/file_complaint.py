from app.services.complaint_service import ComplaintService
from fastapi import Depends

class FileComplaintUseCase:
    def __init__(self, complaint_service: ComplaintService = Depends()):
        self.complaint_service = complaint_service

    async def file_complaint(self, data: dict):
        return await self.complaint_service.file_complaint(data)
