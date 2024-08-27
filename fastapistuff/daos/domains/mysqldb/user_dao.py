from daos.domains.mysqldb.db import ServiceDB
from daos.models.users import User
from typing import Mapping
from uuid import UUID

class UserDAO:
    def __init__(self, connection: ServiceDB) -> None:
        self.servicedb = connection

    def get_user_by_id(self, user_id: UUID) -> User | None:
        query = "SELECT * FROM users WHERE uuid = %s"
        cursor = self.servicedb.get_cursor()

        try:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
        except Exception as e:
            print(f"[UserDAO] A DB error occurred: {e}")
            raise e
        finally:
            cursor.close()
        return self._unmarshal_user(result)

    def get_user_by_username(self, username: str) -> User | None:
        query = "SELECT * FROM users WHERE username = %s"
        cursor = self.servicedb.get_cursor()
        
        try:
            cursor.execute(query, (username,))
            result = cursor.fetchone()
        except Exception as e:
            print(f"[UserDAO] A DB error occurred: {e}")
            raise e
        finally:
            cursor.close()
        return self._unmarshal_user(result)

    def create_user(self, name: str) -> User | None:
        query = "INSERT INTO users (username) VALUES (%s)"
        cursor = self.servicedb.get_cursor()
        
        if len(name) > 255:
            raise ValueError(f"Name is too long: {len(name)} characters (max 255)")
        
        try:
            cursor.execute(query, (name,))
            self.servicedb.commit()
        except Exception as e:
            self.servicedb.rollback()
            print(f"[UserDAO] A DB error occurred: {e}")
            raise e
        finally:
            cursor.close()
        return self.get_user_by_username(name)

    def update_user(self, user_id: UUID, username: str) -> User | None:
        query = "UPDATE users SET username = %s WHERE uuid = %s"
        cursor = self.servicedb.get_cursor()
        
        if len(username) > 255:
            raise ValueError(f"Name is too long: {len(username)} characters (max 255)")
        
        try:
            cursor.execute(query, (username, user_id))
            self.servicedb.commit()
        except Exception as e:
            self.servicedb.rollback()
            print(f"[UserDAO] A DB error occurred: {e}")
            raise e
        finally:
            cursor.close()
        return self.get_user_by_id(user_id)

    def delete_user(self, user_id: UUID) -> bool:
        query = "DELETE FROM users WHERE uuid = %s"
        cursor = self.servicedb.get_cursor()
        affected_rows = 0

        try:
            cursor.execute(query, (user_id,))
            self.servicedb.commit()
            affected_rows = cursor.rowcount
        except Exception as e:
            self.servicedb.rollback()
            print(f"[UserDAO] A DB error occurred: {e}")
            raise e
        finally:
            cursor.close()
        return affected_rows > 0
        

    def _unmarshal_user(self, db_record: Mapping | None) -> User | None:
        if not db_record:
            return None
        return User(**db_record)