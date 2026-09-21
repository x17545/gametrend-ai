from fastapi import APIRouter, HTTPException

from app.models.data import DataCreate, DataUpdate
from app.services.data_service import (
    create_data,
    delete_data,
    get_all_data,
    get_data_summary,
    update_data,
)


router = APIRouter(
    prefix="/api/data",
    tags=["Data"],
)


@router.post("")
def add_data(data: DataCreate):
    return create_data(data)


@router.get("")
def list_data():
    return get_all_data()


@router.get("/summary")
def data_summary():
    return get_data_summary()


@router.put("/{data_id}")
def edit_data(data_id: str, data: DataUpdate):
    result = update_data(data_id, data)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Data not found",
        )

    return result


@router.delete("/{data_id}")
def remove_data(data_id: str):
    success = delete_data(data_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Data not found",
        )

    return {
        "message": "Data deleted successfully",
        "id": data_id,
    }