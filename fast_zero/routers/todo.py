from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User, Todo
from fast_zero.schemas import TodoPublic, TodoSchema
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