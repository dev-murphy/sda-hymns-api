from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, col, select
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

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

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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

@app.get("/")
def read_root():
    return {"message": "Welcome to SDA Hymnal API"}

@app.get("/hymns/")
@limiter.limit("50/minute")
async def read_hymns(
    request: Request,
    session: SessionDep,
    categories: str | None = None,
    sort: str = "",
    offset: int = 0,
    limit: Annotated[int, Query(le=10)] = 10,
) -> dict[str, int | list[Hymns]]:
    statement = select(Hymns)

    if categories is not None:
        category_list = categories.split(":")
        if len(category_list) == 1:
            statement = statement.where(Hymns.category == category_list[0])
        elif len(category_list) == 2:
            statement = statement.where(Hymns.category == category_list[0]).where(Hymns.subcategory == category_list[1])
    
    if sort == "Page Title (Asc)":
        statement = statement.order_by(Hymns.title.asc())
    elif sort == "Page Title (Desc)":
        statement = statement.order_by(Hymns.title.desc())
    elif sort == "Page No. (Desc)":
        statement = statement.order_by(Hymns.hymn_number.desc())
    
    statement = statement.offset(offset).limit(limit)
    result = session.exec(statement).all()

    count = session.scalar(select(func.count()).select_from(Hymns))
    return { "count": count, "hymns": result }

@app.get("/hymns/{hymn_no}")
@limiter.limit("50/minute")
async def read_hymn(
    request: Request,
    hymn_no: int, 
    session: SessionDep
) -> Hymns:
    hymn = session.get(Hymns, hymn_no)
    if not hymn:
        raise HTTPException(status_code=404, detail="Hymn not found")
    return hymn

@app.get("/categories/")
@limiter.limit("50/minute")
async def read_categories(
    request: Request,
    session: SessionDep
) -> list[str]:
    categories = session.exec(select(Hymns.category).distinct()).all()
    return categories

@app.get("/subcategories/")
@limiter.limit("50/minute")
async def read_subcategories(
    request: Request,
    session: SessionDep
) -> list[str]:
    subcategories = session.exec(select(Hymns.subcategory).distinct()).all()
    subcategories = [subcategory for subcategory in subcategories if subcategory is not None]
    return subcategories