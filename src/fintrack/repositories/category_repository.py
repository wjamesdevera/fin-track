from fintrack.models.models import Category
from fintrack.db import engine
from sqlmodel import Session, select


class CategoryRepository():

    def __init__(self):
        pass

    def add(self, name: str) -> Category | None:
        with Session(engine) as session:
            new_category = Category(name=name)
            session.add(new_category)
            return session.commit()

    def find_by_name(self, name: str):
        with Session(engine) as session:
            stmt = select(Category).where(Category.name == name)
            result = session.exec(stmt)
            return result.one_or_none()

    def change_name(self, old_name: str, new_name) -> None:
        with Session(engine) as session:
            old_category = self.find_by_name(old_name)

            # check if new_name already exists
            if self.find_by_name(new_name):
                print(
                    f"Modifying: {old_name} failed: category {new_name} already exists")
                return
            old_category.name = new_name
            session.add(old_category)
            session.commit()

    def delete(self, name: str) -> None:
        with Session(engine) as session:
            category_to_delete = self.find_by_name(name)
            if not category_to_delete:
                print(
                    f"Deleting: {name} failed: category {name} does not exist.")
                return
            session.delete(category_to_delete)
            session.commit()
            print(f"Deleted: Category={name}")
