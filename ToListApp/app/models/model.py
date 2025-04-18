import uuid
import datetime 
from typing import List,Optional
from pydantic import BaseModel
class ModelCreateRequest(BaseModel):
    title:str
    description:str
    todo:datetime.datetime
    done:bool| None =False
class ModelUdateReqest(BaseModel):
    title:Optional[str] = None
    description:Optional[str]= None
    todo:Optional[datetime.datetime]= None
    done:Optional[bool] | None =False
class ModelResponse(BaseModel):
    id:uuid.UUID
    title:Optional[str] = None
    description:Optional[str]= None
    todo:Optional[datetime.datetime]= None
    done: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime | None
class ModelListResponse(BaseModel):
   items:List[ModelResponse] 
   