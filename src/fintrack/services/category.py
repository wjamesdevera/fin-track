from fintrack.models.category import Category
from sqlmodel import Session, select


def add_category(name: str, session: Session) -> Category | None:
    added = Category(name=name)
    session.add(added)
    session.commit()
    print(f"Added: Category={name}")
    return (added)


def find_category(name: str, session: Session):
    stmt = select(Category).where(Category.name == name)
    result = session.exec(stmt)
    return result.one_or_none()


def update_category(old_name: str, new_name: str, session: Session) -> None:
    old_category = find_category(old_name, session)

    # check if new_name already exists
    if find_category(new_name, session):
        print(
            f"Modifying: {old_name} failed: category {new_name} already exists")
        return
    old_category.name = new_name
    session.add(old_category)
    session.commit()
    print(f"Modified: Category={old_name} -> Category={new_name}")
    return old_category


def delete_category(name: str, session: Session) -> None:
    category_to_delete = find_category(name, session)
    if not category_to_delete:
        print(
            f"Deleting: {name} failed: category {name} does not exist.")
        return
    session.delete(category_to_delete)
    session.commit()
    print(f"Deleted: Category={name}")
    return category_to_delete
