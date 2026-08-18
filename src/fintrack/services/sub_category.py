from typing import Optional

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


def find_sub_category(name: str, session: Session):
    return session.exec(select(SubCategory).where(SubCategory.name == name)).one_or_none()
