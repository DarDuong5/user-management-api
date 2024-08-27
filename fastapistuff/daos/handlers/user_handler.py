from fastapi import HTTPException
from daos.domains.mysqldb.user_dao import UserDAO
from daos.models.users import User, CreateUser, UpdateUser, DeleteUser
from pymysql.err import IntegrityError

class UserHandler:
    def __init__(self, user_dao: UserDAO) -> None:
        self.user_dao = user_dao

    async def create_user(self, user: CreateUser) -> User | None:
        try:
            created_user = self.user_dao.create_user(user.username)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="User already exists.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while creating the user: {e}")
        
        return created_user

    async def update_user(self, user: UpdateUser) -> User | None:
        try:
            updated_user = self.user_dao.update_user(user.username)
        except IntegrityError:
            raise HTTPException(status_code=404, detail="User not found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the user: {e}")
        
        return updated_user

    async def delete_user(self, user: DeleteUser) -> User | None:
        try:
            deleted_user = self.user_dao.delete_user(user.username)
        except IntegrityError:
            raise HTTPException(status_code=404, detail="User not found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while deleting the user: {e}")
        
        return deleted_user
