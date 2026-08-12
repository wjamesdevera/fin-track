from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
from sqlmodel import Field, Relationship
from .core import SimpleIDModel, UUIDIDModel, TimestampModel


class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"


class Category(SimpleIDModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str

    sub_categories: list["SubCategory"] | None = Relationship(
        back_populates="category")


class SubCategory(SimpleIDModel, table=True):
    __tablename__ = "sub_categories"
    name: str

    category_id: int | None = Field(default=None, foreign_key="categories.id")
    category: Category | None = Relationship(back_populates="sub_categories")

    transactions: list["Transaction"] | None = Relationship(
        back_populates="sub_category")


class Transaction(UUIDIDModel, TimestampModel, table=True):
    __tablename__ = "transactions"
    type: TransactionType
    note: str | None = Field(default=None)
    sub_category: SubCategory | None = Relationship(
        back_populates="transactions")
    sub_category_id: int | None = Field(
        default=None, foreign_key="sub_categories.id")
    amount: Decimal = Field(default=0, max_digits=11, decimal_places=2)


class Account(UUIDIDModel, TimestampModel, table=True):
    __tablename__ = "accounts"
    balance: Decimal = Field(default=0, max_digits=11, decimal_places=2)
