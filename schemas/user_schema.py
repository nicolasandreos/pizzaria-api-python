from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool] = None
    admin: Optional[bool] = None

    # permite que o scjhema seja criado a partir dos atributos de um objeto
    class Config:
        from_attributes = True
