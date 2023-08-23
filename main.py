from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id_user: int
    name: str
    email: str
    password: str

user = User(id_user=1, name='john conor', email='Judgment_Day@mail.com', password='skynet')
users = [user]




@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello_user/", response_class=HTMLResponse)
async def say_hello(request: Request):
    return templates.TemplateResponse('hello.html', {'request': request, 'title': 'Hello', 'users': users})

@app.post("/adding/")
async def adding_user(new_user: User):
    users.append(new_user)
    return new_user


@app.put("/change/{id}")
async def change(id:int, new_user: User):
    for item in users:
        if item.id_user == id:
            item.id_user = new_user.id_user
            return item

@app.delete("/del/{id}")
async def del_user(id:int):
    for item in users:
        if item.id_user == id:
            users.remove(item)
            return item

