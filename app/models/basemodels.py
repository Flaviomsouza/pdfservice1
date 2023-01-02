from datetime import date
from typing import Optional
from pydantic import BaseModel

class User_(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    hash: Optional[str]
    is_admin: Optional[bool]
    is_collaborator: Optional[bool]

class User_For_View_(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    is_admin: Optional[bool]
    is_collaborator: Optional[bool]

class Worksheet_For_View_(BaseModel):
    id: Optional[int]
    title: Optional[str]
    creation_date: Optional[date]
    image_id: Optional[str]