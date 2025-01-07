from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, col, select

class Hymns(SQLModel, table=True):
    hymn_number: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    stanzas: str
    category: str
    subcategory: str = Field(nullable=True)
    first_line: str = Field(nullable=True)
    published_at: str = Field(nullable=True)
    key: str = Field(nullable=True)
    filename: str = Field(nullable=True)
    composer: str = Field(nullable=True)
    author: str = Field(nullable=True)


sqlite_file_name = "hymns.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/hymns/")
def read_hymns(
    session: SessionDep,
    categories: str | None = None,
    sort: str = "",
    q: str = "",
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hymns]:
    statement = select(Hymns)

    if q.isdigit():
        statement = statement.where(Hymns.hymn_number == int(q))
    elif q != "":
        statement = statement.where(col(Hymns.title).regexp_match(q, 'i'))

    if categories is not None:
        category_list = categories.split(":")
        if len(category_list) == 1:
            statement = statement.where(Hymns.category == category_list[0])
        elif len(category_list) == 2:
            statement = statement.where(Hymns.category == category_list[0]).where(Hymns.subcategory == category_list[1])
    
    sort_order = Hymns.hymn_number.asc()
    if "Page Title (Asc)" in sort:
        sort_order = Hymns.title.asc()
    elif "Page Title (Desc)" in sort:
        sort_order = Hymns.title.desc()
    elif "Page No. (Desc)" in sort:
        sort_order = Hymns.hymn_number.desc()

    statement = statement.order_by(sort_order).offset(offset).limit(limit)

    hymns = session.exec(statement).all()
    return hymns

@app.get("/hymns/{hymn_no}")
def read_hymn(
    hymn_no: int, 
    session: SessionDep
) -> Hymns:
    hymn = session.get(Hymns, hymn_no)
    if not hymn:
        raise HTTPException(status_code=404, detail="Hymn not found")
    return hymn
