from fastapi import APIRouter, Response, status
from config.db import conn
from schema.user import users_entity, user_entity
from models.user import User, UpdateUser
from starlette.status import HTTP_204_NO_CONTENT
from typing import List

# modulo para cifrar contaseñas
from passlib.hash import sha256_crypt
from bson import ObjectId


user_router = APIRouter()


@user_router.get("/", response_model=List[User], tags=["Users"])
def find_all_users():
    return users_entity(conn.local.user.find())


@user_router.get("/{id}", response_model=User, tags=["Users"])
def find_user(id: str):
    find_user_by_id = user_entity(conn.local.user.find_one({"_id": ObjectId(id)}))
    print(find_user_by_id)
    return find_user_by_id


@user_router.post("/", response_model=User, tags=["Users"])
def create_user(user: User):
    new_user = dict(user)
    # cifrar la contraseña
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    del new_user["id"]

    idx = conn.local.user.insert_one(new_user).inserted_id
    find_user = conn.local.user.find_one({"_id": idx})
    return user_entity(find_user)


@user_router.put("/{id}", response_model=User, tags=["Users"])
def update_user(id: str, user: UpdateUser):
    conn.local.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
    return user_entity(conn.local.user.find_one({"_id": ObjectId(id)}))


@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id: str):
    user_entity(conn.local.user.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)
