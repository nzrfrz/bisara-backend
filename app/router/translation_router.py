from fastapi import APIRouter, Depends, UploadFile, File

from ..models.translation_model import TranslationResponse
from ..controllers.translation_controller import translation_controller

router = APIRouter()

@router.post('/translation/text', response_model=TranslationResponse)
async def translation_route(payload: TranslationResponse, sourceLang: str | None = None, targetLang: str | None = None):
  return await translation_controller(payload, sourceLang, targetLang)