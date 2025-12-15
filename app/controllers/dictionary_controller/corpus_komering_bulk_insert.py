import csv
import io
# import json
from datetime import datetime
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from ..._utils.database import db
from ..._utils.query_manager import insert_many_chunked

COLLECTION = db["corpus_komering"]

async def corpus_komering_bulk_insert(file: UploadFile):
  try:
    contents = await file.read()
    csv_text = contents.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(csv_text), delimiter=",")

    now = datetime.now()
    inserted_data=[]

    for row_index, row in enumerate(reader, start=1):
      if len(row) < 2:
        print(f"Skipping row {row_index}: {row}")
        continue

      indonesia = row[0].strip().lower()
      komering_list = [
        item.strip().lower()
        for item in row[1].split(",")
        if item.strip()
      ]

      if komering_list and isinstance(komering_list[0], list):
        komering_list = [item for sub in komering_list for item in sub]

      if not indonesia or not komering_list:
        continue

      doc = {
        "indonesia": indonesia,
        "komering": komering_list,
        "status": "VALID",
        "createdAt": now,
        "updatedAt": now
      }

      inserted_data.append(doc)

    results = await insert_many_chunked(COLLECTION, inserted_data)
    # print("lampung added: \n", json.dumps(inserted_data[:5], indent=2, default=str))

    return JSONResponse(
      status_code=status.HTTP_200_OK,
      content={
        "status": 200,
        "message": f"{results} Corpus Komering successfully inserted",
        "data": {}
      }
    )
  except Exception as error:
    print("error corpus komering bulk insert: \n", error)
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=str(error)
    )
    