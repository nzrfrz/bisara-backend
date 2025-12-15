from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# 1) Registration payload (request body)
class CorpusKomeringBase(BaseModel):
  indonesia: Optional[str] = None
  komering: Optional[str] = None
  status: Optional[str] = None

# 2) DB representation (what you store in Mongo)
class CorpusKomeringMutable(CorpusKomeringBase):
  pass

# 3) What you return to the client
class CorpusKomering(CorpusKomeringBase):
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