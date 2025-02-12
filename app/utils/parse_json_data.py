import json
from fastapi import Form, HTTPException
from app.models.schemas.complaint_schemas import ComplaintCreateSchema

async def parse_complaint_data(complaint_data: str = Form(...)) -> ComplaintCreateSchema:
    try:
        data_dict = json.loads(complaint_data)
        return ComplaintCreateSchema(**data_dict)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in complaint_data")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))