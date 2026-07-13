# from fastapi import APIRouter # type: ignore
# from app.repositories.user_repository import create_user
# from app.core.security import hash_password

# router = APIRouter()

# @router.post("/create-user")
# async def test_user():

#     user = {
#         "name": "Shivam",
#         "email": "shivam@test.com",
#         "password": "123456"
#     }

#     user_id = await create_user(user)

#     return {
#         "id": str(user_id), 
#         "user" : str(user)
#     }

# @router.get("/hash")
# async def hash_test():

#     password = "123456"

#     return {
#         "hash": hash_password(password)
#     }