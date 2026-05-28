from symtable import Class
from requests import Session
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        