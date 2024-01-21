from fastapi import HTTPException
from repositories.todos import TodoRepo
from schemas.todo import Todo, TodoCreate, TodoUpdate
from models.todo import TodoDB


class TodoServices():

    def __init__(self, db) -> None:
        self.repo = TodoRepo(db=db)

    def get_all_todos(self) -> list[Todo]:
        all_todos_from_db = self.repo.get_all()
        result = [Todo.from_orm(item) for item in all_todos_from_db]
        return result

    def create_new(self, todo_create: TodoCreate) -> Todo:
        new_item_from_db = self.repo.create(todo_create)
        todo_create = Todo.from_orm(new_item_from_db)
        return todo_create

    def get_by_id(self, id: int) -> Todo:
        todo_item = self.repo.get_by_id(id)
        return Todo.from_orm(todo_item)

    def update(self, id: int, todo_update: TodoUpdate) -> Todo:
        existing_todo = self.repo.get_by_id(id)
        if not existing_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        updated_todo = self.repo.update(id, todo_update)
        return Todo.from_orm(updated_todo)

    def delete(self, id: int) -> bool:
        existing_todo = self.repo.get_by_id(id)
        if not existing_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        self.repo.delete(id)
        return True
