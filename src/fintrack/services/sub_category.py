from fintrack.models.category import SubCategory, Category
from sqlmodel import Session


class SubCategoryExist(Exception):
    pass


def add_sub_category(category: Category, name: str, session: Session) -> SubCategory:
    for sc in category.sub_categories:
        if sc.name == name:
            raise SubCategoryExist

    new_sc = SubCategory(name=name, category=category)
    session.add(new_sc)
    session.commit()
    print(f'Successfully added: Subcategory={name}')
    return new_sc
