from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_zero.security import get_current_user, get_password_hash

router = APIRouter(
    prefix='/users',  # atalho
    tags=['users'],
)
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=UserPublic
)  # Modelo de contrato de saída, retorno
def create_user(
    user: UserSchema, session: T_Session
):  # modelo de contrato de entrada
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )  # scalar da um select em User onde username é igual ao username recebido
    if db_user:  # se já existe o user, retorna erro
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )
    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
    )
    session.add(db_user)
    session.commit()  # valida se essa operação aconteceu
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def read_users(
    session: T_Session,
    limit: int = 10,  # limita a quantidade de busca no select
    skip: int = 0,
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)  # {variável} na url
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
