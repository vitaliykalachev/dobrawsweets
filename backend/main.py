
from fastapi import FastAPI
import jwt
from passlib.hash import bcrypt

from pydantic import BaseModel
from tortoise import fields
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

JWT_SECRET = "myjwsecret"




app = FastAPI()

class Task(BaseModel):
    id: str
    content: str
    
class Tasks(BaseModel):
    __root__:dict[str, Task]
    
class Column(BaseModel):
    id: str
    title: str
    taskIds: list
class Columns(BaseModel):
    __root__: dict[str, Column]
    
class Board(BaseModel):
    tasks: Tasks
    columns: Columns
    columnOrder: list
    
    
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password = fields.CharField(200)
    board = fields.JSONField(default='{"tasks": {}, "columns": {}, "columnOrder": []}')
    
    def vrify_password(self, password):
        return bcrypt.verify(password, self.password)
    
User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


@app.get('/board')
async def get_board():
    user = await User.get(id=1)
    return {'board': user.board}

@app.post('/board')
async def save_board(board: Board):
    user = await User.get(id=1)
    user.board = board.json()
    await user.save()
    return{"status": "success"}

@app.post('/users')
async def create_user(user_in: UserIn_Pydantic):
    user = User(username=user_in.username, password=bcrypt.hash(user_in.password))
    await user.save()
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return{'access_token': token}


register_tortoise(
    app,
    # db_url='postgres://postgres:Password1@localhost:5432/postgres',
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)