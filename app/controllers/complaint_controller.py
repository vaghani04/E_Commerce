from fastapi import HTTPException, status, Depends
from app.usecases.complaints.file_complaint import FileComplaintUseCase
from app.usecases.complaints.get_complaints import GetComplaintsUsecase

class ComplaintController:
    def __init__(self, file_complaint_usecase: FileComplaintUseCase = Depends(),
                 get_complaints_usecase: GetComplaintsUsecase = Depends()):
        self.file_complaint_usecase = file_complaint_usecase
        self.get_complaints_usecase = get_complaints_usecase

    async def file_complaint(self, data: dict):
        if data["current_user"]["role"] == "seller":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Buyers can file complaints.")
        return await self.file_complaint_usecase.file_complaint({
            "user_id": data["current_user"]["sub"],
            "complaint_data": data["complaint_data"],
            "file": data["file"]
        })
    
    async def get_complaints(self, data: dict):
        if data["current_user"]["role"] == "buyer":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Sellers can get all complaints.")
        return await self.get_complaints_usecase.get_complaints({"user_id": data["current_user"]["sub"]})
            
    async def get_complaint_by_id(self, data: dict):
        if data["current_user"]["role"] == "buyer":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Sellers can get all complaints.")
        return await self.get_complaints_usecase.get_complaint_by_id({"user_id": data["current_user"]["sub"], "complaint_id": data["complaint_id"]})