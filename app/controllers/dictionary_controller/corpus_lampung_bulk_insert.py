import csv
import io
from datetime import datetime
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from ..._utils.database import db
from ..._utils.query_manager import insert_many_chunked

COLLECTION = db["corpus_lampung"]

async def corpus_lampung_bulk_insert(file: UploadFile):
  try:
    contents = await file.read()
    csv_text = contents.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(csv_text), delimiter=";")

    now = datetime.now()
    inserted_data=[]

    for row_index, row in enumerate(reader, start=1):
      if len(row) < 2:
        print(f"Skipping row {row_index}: {row}")
        continue

      indonesia = row[0].strip().lower()
      lampung_list = [ col.strip().lower() for col in row[1:] if col and col.strip() ]

      if not indonesia or not lampung_list:
        continue

      doc = {
        "indonesia": indonesia,
        "lampung": lampung_list,
        "status": "VALID",
        "createdAt": now,
        "updatedAt": now
      }

      inserted_data.append(doc)

    results = await insert_many_chunked(COLLECTION, inserted_data)
    # print("lampung added: \n", json.dumps(inserted_data, indent=2, default=str))

    return JSONResponse(
      status_code=status.HTTP_200_OK,
      content={
        "status": 200,
        "message": f"{results} Corpus Lampung successfully inserted",
        "data": {}
      }
    )
  except Exception as error:
    print("error corpus lampung bulk insert: \n", error)
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=str(error)
    )
    