import uuid 
import datetime
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.engine import Item
from app.models.model import ModelCreateRequest,ModelListResponse,ModelResponse,ModelUdateReqest
from app.utils.utils import get_db
router = APIRouter(prefix="/items",tags=["items"])
@router.post("/")
async def crete_items(item:ModelCreateRequest,db:Session=Depends(get_db))->ModelResponse:
    new_model = Item(**item.dict())
    new_model.id = uuid.uuid4()
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model
@router.get("/")
async def get_model(db:Session=Depends(get_db))->ModelListResponse:
    model = db.query(Item).all()
    return {"items":model}
@router.get("/{items_id}")
async def get_model(mode_id:uuid.UUID,db:Session=Depends(get_db))->ModelResponse:
    model = db.query(Item).filter(Item.id==mode_id).first()
    if not model:
        raise HTTPException(status_code=404,detail="Not items")
    return model
@router.put("/{items_id}")
async def udate_model(mode_id:uuid.UUID,model_udate:ModelUdateReqest,db:Session=Depends(get_db))->ModelResponse:
    model = db.query(Item).filter(Item.id==mode_id).first()
    if not model:
        raise HTTPException(status_code=404,detail="Not items")
    for key,value in model_udate.dict(exclude_unset=True).items():
        setattr(model, key, value)
    db.commit()
    db.refresh(model)
    return model
@router.delete("/{items_id}")
async def delete_item(mode_id:uuid.UUID,db:Session=Depends(get_db)):
    model = db.query(Item).filter(Item.id==mode_id).first()
    if not model:
        raise HTTPException(status_code=404,detail="Not items")
    db.delete(model)
    db.commit()
    return model