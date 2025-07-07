from sqlalchemy import Column, String, Integer, DateTime 
from datetime import datetime
from typing import Union

from  model import Base

class Client(Base):
    __tablename__ = 'clients'

    id = Column("pk_client", Integer, primary_key=True)
    name = Column(String(140))
    email = Column(String(140), unique=True)
    phone = Column(String(20))
    document = Column(String(30))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def __init__(self, name:str, email:int, phone:float, document:Union[DateTime, None] = None):
        
        self.name = name
        self.email = email
        self.phone = phone
        self.document = document

