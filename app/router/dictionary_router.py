from fastapi import APIRouter, Depends, UploadFile, File

from ..models.corpus_lampung_model import CorpusLampung, CorpusLampungMutable
from ..models.corpus_komering_model import CorpusKomering, CorpusKomeringMutable

from ..controllers.dictionary_controller.corpus_lampung_bulk_insert import corpus_lampung_bulk_insert
from ..controllers.dictionary_controller.corpus_lampung_pagination import corpus_lampung_pagination

from ..controllers.dictionary_controller.corpus_komering_bulk_insert import corpus_komering_bulk_insert
from ..controllers.dictionary_controller.corpus_komering_pagination import corpus_komering_pagination

router = APIRouter()

@router.post('/corpus-bulk-insert/lampung/', response_model=CorpusLampung)
async def corpus_lampung_bulk_insert_route(file: UploadFile = File(...)):
  return await corpus_lampung_bulk_insert(file)

@router.get('/corpus-list/lampung', response_model=CorpusLampung)
async def corpus_lampung_pagination_route(page: int = 1, limit: int = 10, status: str | None = None, q: str| None = None):
  return await corpus_lampung_pagination(page, limit, status, q)


@router.post('/corpus-bulk-insert/komering/', response_model=CorpusKomering)
async def corpus_komering_bulk_insert_route(file: UploadFile = File(...)):
  return await corpus_komering_bulk_insert(file)

@router.get('/corpus-list/komering', response_model=CorpusKomering)
async def corpus_komering_pagination_route(page: int = 1, limit: int = 10, status: str | None = None, q: str| None = None):
  return await corpus_komering_pagination(page, limit, status, q)