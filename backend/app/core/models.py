from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase


# Database layer
#-------------------------------------------------------------------------------

class Base(DeclarativeBase):
    pass


# Transport layer
#-------------------------------------------------------------------------------

class Message(BaseModel):
    message: str
