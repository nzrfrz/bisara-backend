from fastapi import Header, HTTPException, status

from .._utils.jwt_manager import header_token_verifier

async def header_auth_checker(authorization: str = Header(None)):
  if not authorization:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Missing Authorization header",
    )
  
  if not authorization.startswith("Bearer "):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid Authorization header format",
    )
  
  token = authorization.split(" ")[1]
  
  try:
    decoded = header_token_verifier(token)
    print('decoded: \n', decoded)
  except Exception:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Token Expired"
    )
  
  user_id = decoded.get("_id")
  if not user_id:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Token payload invalid"
    )
  
  return str(user_id)
