import re
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from .._utils.database import db

COLLECTION_KOMERING = db["corpus_komering"]
COLLECTION_LAMPUNG = db["corpus_lampung"]

NO_TRANSLATION_FLAG = "Belum ada terjemahan untuk kata ini."

async def translation_controller(payload, sourceLang, targetLang):
  try:
    source_text = payload.sourceText.lower().strip()
    text_lower = source_text.lower()

    source_lang = sourceLang or "indonesia"
    target_lang = (targetLang or "").strip().lower()

    # 🔁 Detect translation mode
    is_reverse = source_lang in ("lampung", "komering") and target_lang == "indonesia"

    # 🗃 Select collection & fields
    if source_lang == "indonesia":
      collection = COLLECTION_LAMPUNG if targetLang == 'lampung' else COLLECTION_KOMERING
      source_field = "indonesia"
      target_field = target_lang
    elif source_lang == "lampung":
      collection = COLLECTION_LAMPUNG
      source_field = "lampung"
      target_field = "indonesia"
    elif source_lang == "komering":
      collection = COLLECTION_KOMERING
      source_field = "komering"
      target_field = "indonesia"
    else:
      raise HTTPException(status_code=400, detail="Unsupported sourceLang")

    # 1️⃣ Tokenize while keeping punctuation
    # Example: "tidur," → ["tidur", ","]
    tokens = re.findall(r"\w+|[^\w\s]", text_lower)

    full_translation_parts: list[str] = []
    other_translations = []

    for token in tokens:
      # If punctuation, just append it to full translation
      if re.fullmatch(r"[^\w\s]", token):
        full_translation_parts.append(token)
        continue

      # 🔎 Query logic differs by mode
      if is_reverse:
        # array field match
        doc = await collection.find_one({
          source_field: token,
          'status': "VALID"
        })
      else:
        doc = await collection.find_one({
          source_field: token,
          'status': "VALID"
        })

      if doc and target_field in doc:
        translations = doc[target_field]

        # normalize
        if isinstance(translations, list):
          chosen = translations[0]
        else:
          chosen = translations

        full_translation_parts.append(chosen)

        if not is_reverse:
          other_translations.append({
            token: translations if isinstance(translations, list) else [translations],
            "flag": None
          })
      else:
        full_translation_parts.append(token)

        if not is_reverse:
          other_translations.append({
            token: [token],
            "flag": NO_TRANSLATION_FLAG
          })

    # 🧩 Rebuild sentence
    full_text_translation = ""
    for i, part in enumerate(full_translation_parts):
      if i > 0 and not re.fullmatch(r"[^\w\s]", part):
        full_text_translation += " "
      full_text_translation += part
    
    # print('payload translation: ', full_text_translation)

    # 🧾 Build response (mode-aware)
    if is_reverse:
      data = {
        "sourceText": source_text,
        "sourceLang": source_lang,
        "targetLang": target_lang,
        "fullTextTranslation": full_text_translation
      }
    else:
      data = {
        "sourceText": source_text,
        "sourceLang": source_lang,
        "targetLang": target_lang,
        "fullTextTranslation": full_text_translation,
        "otherTranslation": other_translations
      }
    
    response = JSONResponse(
      status_code=status.HTTP_200_OK,
      content={
        "status": 200,
        "message": "Translation success",
        "data": data
      }
    )
    return response
  except Exception as error:
    print("error translation: \n", error)
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=str(error)
    )