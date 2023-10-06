from datetime import timedelta
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Depends, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
    OAuth2PasswordRequestForm,
)
from jose import JWTError, jwt

from db import DBCollection, get_collection
from models import CreateUserSchema, User, UserSchema
from scopes import DEFAULT_USER_SCOPES, APIScope
from settings import default_settings
from utils.auth import get_password_hash, create_access_token

auth_router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/access-token",
    scopes={"all": "Provides super user permission to all endpoints provided by Plixa"},
)


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    user_collection = get_collection(DBCollection.USER)
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            default_settings.JWT_SETTINGS.SECRET_KEY,
            algorithms=[default_settings.JWT_SETTINGS.ALGORITHM],
        )
        user_id: str = payload.get("subject").get("user_id")
        token_scopes = payload.get("subject").get("scopes", [])
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise credentials_exception
    if "all" in token_scopes:
        return User.model_load(user)
    for scope in [scope for scope in security_scopes.scopes if scope != "all"]:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return User.model_load(user)


@auth_router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: Annotated[
        User,
        Security(get_current_user, scopes=[APIScope.ALL, APIScope.CREATE_USER]),
    ],
    user_data: CreateUserSchema,
):
    # TODO: Protect this endpoint
    user_collection = get_collection(DBCollection.USER)
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="password mismatch"
        )
    user_exist = await user_collection.find_one({"email": user_data.email})
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="user with this email address already exist",
        )
    user_data = user_data.model_dump(exclude={"confirm_password"})
    user_data["password"] = get_password_hash(user_data["password"])
    user = User(**user_data)
    user = await user_collection.insert_one(user.model_dump())
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return UserSchema(**User.model_load(new_user).model_dump())


@auth_router.post("/access-token")
async def get_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # TODO: Provide both refresh and access token
    user = await User.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=default_settings.JWT_SETTINGS.EXPIRES_DELTA
    )
    token_data = {
        "subject": {
            "user_id": user.id,
            "scopes": list(DEFAULT_USER_SCOPES.get(user.type)),
        }
    }
    access_token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}