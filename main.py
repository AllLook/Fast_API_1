import uvicorn
from fastapi import FastAPI, requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()


# templates = Jinja2Templates(directory="./Fast_API_1/templates")


class User(BaseModel):
    user_id: int
    name: str
    email: str
    password: str


users = []  # вместо базы для примера


# user = User(user_id=1, name='john conor', email='Judgment_Day@mail.com', password='skynet')


# user1 = User(name='sara conor', email='Judgment_Day@mail.com', password='skynet')


@app.get("/")
async def root_hello():
    return {"message": "Hello World"}


@app.post("/adding/", response_model=User)
async def adding_user(new_user: User):
    # user = User
    # user.name = new_user.name
    # user.email = new_user.email
    # user.password = new_user.password
    # users.append(user)  #Здесь ошибка что обьект не итерабилен
    users.append(new_user)  # А так оштбки нет
    return new_user


@app.put("/change/{user_id}", response_model=User)
async def change_user(user_id: int, user: User):
    for item in users:
        if item.user_id == user_id:
            item.name = user.name
            return item

    # вернет null если обьекта нет


@app.delete("/take_off/{user_id}", response_model=User)
async def take_off_user(user_id: int):
    for item in users:
        if item.id == user_id:
            users.remove(item)
            return item
    # вернет null если обьекта нет


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )
