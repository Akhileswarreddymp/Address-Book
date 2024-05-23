from fastapi import FastAPI, HTTPException, Depends
from schema import Address, LatLong
from dbconnection import engine, SessionLocal
from sqlalchemy.orm import Session
import models
from sqlalchemy import and_

models.Base.metadata.create_all(bind=engine)

def get_db():
    with SessionLocal() as db:
        yield db

app = FastAPI()

@app.post("/create_address", tags=["Address"])
async def add_address(request: Address, db: Session = Depends(get_db)):
    try:
        address_model = models.AddressTable()
        address_model.name = request.name
        address_model.latitude = request.latitude
        address_model.longitude = request.longitude
        db.add(address_model)
        db.commit()
        return {"msg": "Address added successfully"}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error while adding the address")

@app.get("/get_all_address", tags=["Address"])
async def get_all_address(db: Session = Depends(get_db)):
    try:
        address_data = db.query(models.AddressTable).all()
        if not address_data:
            raise HTTPException(status_code=404, detail="Address not found")
        return address_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_address/{name}", tags=["Address"])
async def get_address_by_name(name: str, db: Session = Depends(get_db)):
    try:
        address_data = db.query(models.AddressTable).filter(models.AddressTable.name == name).all()
        if not address_data:
            raise HTTPException(status_code=404, detail="Address not found")
        return address_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/update_address", tags=["Address"])
async def update_address(request: Address, db: Session = Depends(get_db)):
    try:
        address_data = db.query(models.AddressTable).filter(models.AddressTable.name == request.name).first()
        if not address_data:
            raise HTTPException(status_code=404, detail="Address not found")
        address_data.name = request.name
        address_data.latitude = request.latitude
        address_data.longitude = request.longitude
        db.add(address_data)
        db.commit()
        return {"msg": "Address details updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to update the address")

@app.delete("/delete_address", tags=["Address"])
async def delete_address(name: str, db: Session = Depends(get_db)):
    try:
        address_data = db.query(models.AddressTable).filter(models.AddressTable.name == name).first()
        if not address_data:
            raise HTTPException(status_code=404, detail="Address not found")
        db.delete(address_data)
        db.commit()
        return {"msg": "Address deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get_addresses", tags=["Address"])
async def get_addresses_within_bounds(request: LatLong, db: Session = Depends(get_db)):
    try:
        address_data = db.query(models.AddressTable).filter(
            and_(
                models.AddressTable.latitude >= request.min_latitude,
                models.AddressTable.latitude <= request.max_latitude,
                models.AddressTable.longitude >= request.min_longitude,
                models.AddressTable.longitude <= request.max_longitude
            )
        ).all()
        if not address_data:
            raise HTTPException(status_code=404, detail="Address not found")
        return address_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
