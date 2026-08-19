from typing import Optional, overload

from fintrack.models.category import SubCategory, Category
from sqlmodel import Session, select

from fintrack.db import engine


class SubCategoryExist(Exception):
    pass


def add_sub_category(category: Category, name: str, session: Session) -> SubCategory:
    for sc in category.sub_categories:
        if sc.name == name:
            raise SubCategoryExist

    new_sc = SubCategory(name=name.lower(), category=category)
    session.add(new_sc)
    session.commit()
    print(f'Successfully added: Subcategory={name}')
    return new_sc


def list_all_sub_category(session: Session, category: Optional[Category] = None) -> list[SubCategory]:
    return session.exec(select(SubCategory)).fetchall() if not category else session.exec(select(SubCategory).where(SubCategory.category == category)).fetchall()


@overload
def find_sub_category(session: Session, identifier: str):
    pass


@overload
def find_sub_category(session: Session, identifier: int):
    pass


def find_sub_category(session: Session, identifier: int):
    if type(identifier) is str:
        return session.exec(select(SubCategory).where(SubCategory.name == identifier)).one_or_none()
    if type(identifier) is int:
        return session.get(SubCategory, identifier)


@overload
def delete_sub_category(session: Session, identifier: str) -> SubCategory | None:
    pass


@overload
def delete_sub_category(session: Session, identifier: int) -> SubCategory | None:
    pass


def delete_sub_category(session: Session, identifier: int) -> SubCategory | None:
    subcategory = find_sub_category(session=session, identifier=identifier)
    session.delete(subcategory)
    session.commit()
    return subcategory
