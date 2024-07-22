from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import TodoPublic, TodoSchema, TodoList
from fast_zero.security import get_current_user

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]
# Session é do tipo session do BD que depende do get_session
CurrentUser = Annotated[User, Depends(get_current_user)]
# exige login

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    user: CurrentUser,
    session: Session,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,  # current user
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo

@router.get('/', response_model=TodoList)
def list_todos(
    session: Session,
    user: CurrentUser,
    title: str | None = None,
    description: str | None = None,
    state: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:  # o título contém
        query = query.filter(Todo.title.contains(title))

    if description:  # a description contém
        query = query.filter(Todo.description.contains(description))

    if state:  # o estado é igual
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}