from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.settings import Settings

engine = create_engine(
    Settings().DATABASE_URL
)  # faz a conexão com o banco de dados


def get_session():  # pragma: no cover
    with Session(
        engine
    ) as session:  # cria uma sessão para interagir com o endpoit
        yield session  # yield garante que a session é fechada corretamente no banco
