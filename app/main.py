from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router import user_router, dictionary_router

app = FastAPI()

app = FastAPI(
  title="BhISARA",
  description="Bhineka Aksara Nusantara API",
  version="1.0.0",
  contact={
    "name": "LapazSeturan",
    "email": "lapazseturan@example.com"
  },
  license_info={
    "name": "MIT"
  }
)

# CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://bhisara.vercel.app",
    "https://bhinekaaksaranusantara.vercel.app"
  ],  # adjust later
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(user_router.router, prefix="/api")
app.include_router(dictionary_router.router, prefix="/api")

@app.get("/")
def root():
  return {"message": "Python FastAPI server running"}