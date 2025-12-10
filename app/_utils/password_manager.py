from passlib.context import CryptContext

password_context = CryptContext(
  schemes=["bcrypt_sha256"],
  bcrypt_sha256__rounds=10,
  deprecated="auto"
)

def hash_password(password: str) -> str:
  return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
  return password_context.verify(password, hashed_password)