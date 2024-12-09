from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.users.schemas import SUserRegister
from app.users.dao import UsersDAO
from app.users.auth import get_password_hash
from app.users.auth import authenticate_user, create_access_token
from app.users.models import Users
from app.users.dependencies import get_current_user, get_admin_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth and Users"]
)

@router.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_by_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists") 
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserRegister):
    user = await authenticate_user(user_data.email, user_data.password)  # если юзер есть в базе то создаем токен жвт и отправляем ему в куки
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)  # отправляем токен в куки для дальнейшего использования"booking_access_token", value=access_token, httponly=True)  # отправляем токен в куки для дальнейшего использования
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")  # удаляем токен из куки
    return {"detail": "Logged out"}


@router.get("/me")
async def read_user_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def read_user_all(current_user: Users = Depends(get_admin_current_user)):
    return await UsersDAO.find_all()