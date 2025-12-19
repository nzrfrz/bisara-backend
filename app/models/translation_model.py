from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class TranslationRequest(BaseModel):
  sourceText: str
  source_lang: Optional[str] = None
  target_lang: Optional[str] = None

class TranslationResponse(BaseModel):
  sourceText: str
  source_lang: Optional[str] = None
  target_lang: Optional[str] = None