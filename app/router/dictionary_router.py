from fastapi import APIRouter, Depends, UploadFile, File

from ..models.corpus_lampung_model import CorpusLampung, CorpusLampungMutable

from ..controllers.dictionary_controller.corpus_lampung_bulk_insert import corpus_lampung_bulk_insert
from ..controllers.dictionary_controller.corpus_lampung_pagination import corpus_lampung_pagination

router = APIRouter()

@router.post('/corpus-bulk-insert/lampung/', response_model=CorpusLampung)
async def corpus_lampung_bulk_insert_route(file: UploadFile = File(...)):
  return await corpus_lampung_bulk_insert(file)

@router.get('/corpus-list/lampung', response_model=CorpusLampung)
async def corpus_lampung_pagination_route(page: int = 1, limit: int = 10, status: str | None = None, q: str| None = None):
  return await corpus_lampung_pagination(page, limit, status, q)