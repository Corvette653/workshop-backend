import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/todos"
)

engine = create_engine(DATABASE_URL, echo=True)


class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = False


class TodoCreate(SQLModel):
    title: str


app = FastAPI(title="Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/todos", response_model=list[Todo])
def list_todos():
    with Session(engine) as session:
        return session.exec(select(Todo)).all()


@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    with Session(engine) as session:
        db_todo = Todo(title=todo.title)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo


@app.patch("/todos/{todo_id}", response_model=Todo)
def toggle_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo.done = not todo.done
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        session.commit()
        return {"ok": True}
