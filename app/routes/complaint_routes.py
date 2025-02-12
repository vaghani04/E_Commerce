from fastapi import APIRouter, Depends, UploadFile, File
from typing import Dict
from app.models.schemas.complaint_schemas import ComplaintResponseSchema, ComplaintCreateSchema
from app.controllers.complaint_controller import ComplaintController
from app.usecases.user_auth.verify_access_token import get_current_user
from app.utils.parse_json_data import parse_complaint_data
from typing import List

complaint_router = APIRouter()

@complaint_router.post("/complaints/", response_model=ComplaintResponseSchema)
async def file_complaint(
    complaint_data: ComplaintController = Depends(parse_complaint_data),
    file: UploadFile = File(...),
    complaint_controller: ComplaintController = Depends(),
    current_user: Dict = Depends(get_current_user)
):
    return await complaint_controller.file_complaint({"current_user": current_user, "complaint_data": complaint_data, "file": file})

@complaint_router.get("/complaints", response_model=List[ComplaintResponseSchema])
async def get_complaints(complaint_controller: ComplaintController = Depends(), current_user: Dict = Depends(get_current_user)):
    return await complaint_controller.get_complaints({"current_user": current_user})

@complaint_router.get("/complaints/{complaint_id}", response_model=ComplaintResponseSchema)
async def get_complaint_by_id(complaint_id: str, complaint_controller: ComplaintController = Depends(), current_user: Dict = Depends(get_current_user)):
    return await complaint_controller.get_complaint_by_id({"current_user": current_user, "complaint_id": complaint_id})