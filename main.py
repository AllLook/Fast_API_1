from typing import List
from datetime import date

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import databases
import sqlalchemy

DATABASE_URL = "sqlite:///my_database.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id_user', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(32)),
    sqlalchemy.Column('email', sqlalchemy.String(25)),
    sqlalchemy.Column('password', sqlalchemy.String(10))

)
products = sqlalchemy.Table(
    'products',
    metadata,
    sqlalchemy.Column('id_product', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(32)),
    sqlalchemy.Column('description', sqlalchemy.String(150)),
    sqlalchemy.Column('price', sqlalchemy.Integer)

)
orders = sqlalchemy.Table(
    'orders',
    metadata,
    sqlalchemy.Column('id_order', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('id_user', sqlalchemy.Integer),
    sqlalchemy.Column('id_product', sqlalchemy.Integer),
    sqlalchemy.Column('data_orders', sqlalchemy.DATE),
    sqlalchemy.Column('status_orders', sqlalchemy.Boolean)

)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
metadata.create_all(engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id_user: int
    name: str
    email: str
    password: str
class Product(BaseModel):
    id_product: int
    name: str
    description: str
    price: int

class Order(BaseModel):
    id_order: int
    id_user: int
    id_product: int
    data_orders: date
    status_orders: bool


user = User(id_user=1, name='john conor', email='Judgment_Day@mail.com', password='skynet')
users_list = [user]





@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello_user/", response_class=HTMLResponse)
async def say_hello(request: Request):
    return templates.TemplateResponse('hello.html', {'request': request, 'title': 'Hello', 'users': users_list})


@app.post("/adding/")
async def adding_user(new_user: User):
    users_list.append(new_user)
    return new_user

@app.post("/users/", response_model=User)
async def create_user(user:User):
    query = users.insert().values(**user.model_dump())
    last_record_id = await database.execute(query)
    return {**user.model_dump(), 'id': last_record_id}

@app.get("/users/", response_model= List[User])
async def read_user():
    query = users.select()
    return await database.fetch_all(query)

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    query = users.select().where(users.c.id_user == user_id)
    return await database.fetch_one(query)




@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user:User):
    query = users.update().where(users.c.id_user == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), 'id': user_id}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id_user == user_id )
    await database.execute(query)
    return {'message': 'User delete'}


@app.post("/products/", response_model=Product)
async def create_product(product:Product):
    query = products.insert().values(**product.model_dump())
    last_record_id = await database.execute(query)
    return {**product.model_dump(), 'id': last_record_id}\

@app.get("/products/", response_model= List[Product])
async def read_product():
    query = products.select()
    return await database.fetch_all(query)\

@app.post("/orders/", response_model=Order)
async def create_order(order: Order):
    query = orders.insert().values(**order.model_dump())
    last_record_id = await database.execute(query)
    return {**order.model_dump(), 'id': last_record_id}\

@app.get("/orders/", response_model= List[Order])
async def read_order():
    query = orders.select()
    return await database.fetch_all(query)



@app.put("/change/{id}")
async def change(id: int, new_user: User):
    for item in users_list:
        if item.id_user == id:
            item.id_user = new_user.id_user
            return item


@app.delete("/del/{id}")
async def del_user(id: int):
    for item in users_list:
        if item.id_user == id:
            users_list.remove(item)
            return item

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )