from sqlalchemy import Column,Integer,String,Float
from dbconnection import Base

class AddressTable(Base):
    __tablename__ = "Address"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    