import pymysql
from pymysql.cursors import DictCursor
import os

class ServiceDB:
    def __init__(self) -> None:
        DB_HOST: str = os.getenv('DB_HOST', 'default_host')
        DB_PORT: str = os.getenv('DB_PORT', '0')
        DB_USER: str = os.getenv('DB_USER', 'default_user')
        DB_PASS: str = os.getenv('DB_PASS', 'default_pass')
        DB_NAME: str = os.getenv('DB_NAME', 'default_name')
        
        self.conn = pymysql.connect(
            host=DB_HOST,
            port=int(DB_PORT),
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            autocommit=False,
        )

    def get_cursor(self) -> DictCursor:
        return self.conn.cursor(DictCursor)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()