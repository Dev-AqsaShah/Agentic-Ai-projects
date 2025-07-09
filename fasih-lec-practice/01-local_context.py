from pydantic import BaseModel

class UserInfo(BaseModel):
    name: str 
    age: int
    
user = UserInfo(name="Muhammad Fasih", age=20)

print(user)
