from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    user_name: str
    user_score: float
    user_email:str

class UserDB(User):
    user_password: str
