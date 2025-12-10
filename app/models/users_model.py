from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# 1) Registration payload (request body)
class UserBase(BaseModel):
  credential: Optional[str] = None
  username: Optional[str] = None
  email: Optional[str] = None
  userRole: Optional[str] = None
  password: Optional[str] = None
  accessToken: Optional[str] = None

# 2) DB representation (what you store in Mongo)
class UserMutable(UserBase):
  pass

# 3) What you return to the client
class User(UserBase):
  id: Optional[str] = Field(default=None, alias="_id")
  createdAt: Optional[datetime] = None
  updatedAt: Optional[datetime] = None

  model_config = ConfigDict(
    populate_by_name=True,
    extra="ignore",
    json_encoders={
      datetime: lambda dt: dt.isoformat()
    }
  )