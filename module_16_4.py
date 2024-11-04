from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int = None

@app.get('/users')
async def get_user_page() -> List[User]:
    return users

@app.post('/user/{username}/{age}')
async def add_user(username: str, age: int):
    max_id = max((user.id for user in users), default=0)
    new_user = User(id=max_id + 1, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int):
    for edit_user in users:
        if edit_user.id == user_id:
            edit_user.username = username
            edit_user.age = age
            return edit_user
    raise HTTPException(status_code=404, detail='User was not found')

@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
    for delete_user in users:
        if delete_user.id == user_id:
            users.remove(delete_user)
            return delete_user
    raise HTTPException(status_code=404, detail='User was not found')
