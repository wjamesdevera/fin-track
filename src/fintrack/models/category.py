from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from .core import SimpleIDModel, UUIDIDModel, TimestampModel

if TYPE_CHECKING:
    from fintrack.models.transaction import Transaction


class Category(SimpleIDModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    sub_categories: list["SubCategory"] | None = Relationship(
        back_populates="category")


class SubCategory(SimpleIDModel, table=True):
    __tablename__ = "sub_categories"
    name: str

    category_id: int | None = Field(default=None, foreign_key="categories.id")
    category: Category | None = Relationship(back_populates="sub_categories")

    transactions: list["Transaction"] | None = Relationship(
        back_populates="sub_category")
