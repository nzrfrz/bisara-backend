# from typing import List
from fastapi import APIRouter, Request

from ..controllers.user_controller.user_registration import user_registration
from ..controllers.user_controller.user_login import user_login
from ..controllers.user_controller.user_me import user_me
from ..controllers.user_controller.user_logout import user_logout

from ..models.users_model import User, UserMutable

router = APIRouter()

@router.post('/user/registration/', response_model=User)
async def registration_route(payload: UserMutable):
  return await user_registration(payload)

@router.patch('/user/login/', response_model=User)
async def login_route(payload: User):
  return await user_login(payload)

@router.get('/user/me/', response_model=User)
async def me_route(request: Request):
  return await user_me(request)

@router.get('/user/logout/', response_model=User)
async def logout_route(request: Request):
  return await user_logout(request)