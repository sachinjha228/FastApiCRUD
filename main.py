from fastapi import Depends, FastAPI, Body
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine
import models
import schemas

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

fakeDataBase ={
    1:{'task':"Clean car"},
    2:{'task':"start streaming"},
    3:{'task':"Write blogs"}
}


# @app.get("/")
# def getItems():
#     return fakeDataBase

@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


# @app.get("/{id}")
# def getItemById(id:int):
#     return fakeDataBase[id]

@app.get("/{id}")
def getItem(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item

#Option # 1
# @app.post("/")
# def addItem(task:str):
#     newId = len(fakeDataBase.keys()) + 1
#     fakeDataBase[newId] = {"task":task}
#     return fakeDataBase

@app.post("/")
def addItem(item:schemas.Item, session = Depends(get_session)):
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


# #Option # 2
# @app.post("/")
# def addItem(item:schemas.Item):
#     newId = len(fakeDataBase.keys()) + 1
#     fakeDataBase[newId] = {"task":item.task}
#     return fakeDataBase

# #Option #3
# @app.post("/")
# def addItem(body = Body()):
#    newId = len(fakeDataBase.keys()) + 1
#    fakeDataBase[newId] = {"task":body['task']}
#    return fakeDataBase

# @app.put("/{id}")
# def updateItem(id:int, item:schemas.Item):
#     fakeDataBase[id]['task'] = item.task 
#     return fakeDataBase

@app.put("/{id}")
def updateItem(id:int, item:schemas.Item, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject


# @app.delete("/{id}")
# def deleteItem(id:int):
#     del fakeDataBase[id]
#     return fakeDataBase

@app.delete("/{id}")
def deleteItem(id:int, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted'