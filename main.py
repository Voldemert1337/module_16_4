from fastapi import FastAPI, Path, HTTPException, Body
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str = None
    age: int = None


@app.get('/users')
async def get_users() -> list[User]:
    return users


@app.post('/user/{username}/{age}')
async def add_user(user: User,
                   username: str = Path(min_length=4, max_length=20, description='Enter username', example='NewUser'),
                   age: int = Path(ge=18, le=120, description='Enter User age', example='19')) -> str:
    user.id = 1 if len(users) == 0 else len(users) + 1
    user.username = username
    user.age = age
    users.append(user)
    return f'User {user.id} is registered.'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int,
                      username: str = Path(min_length=4, max_length=20, description='Enter username',
                                           example='NewUser'),
                      age: int = Path(ge=18, le=120, description='Enter User age', example='19')) -> str:
    try:
        edit_user = next(user for user in users if user.id == user_id)
        edit_user.username = username
        edit_user.age = age
        return f'User {user_id} has been updated.'
    except Exception:
        raise HTTPException(status_code=404, detail='User not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> str:
    try:
        del_user = next(user for user in users if user.id == user_id)
        users.remove(del_user)
        return f'User {user_id} has been deleted.'
    except Exception:
        raise HTTPException(status_code=404, detail='User not found')