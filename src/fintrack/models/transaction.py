
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Relationship, Field

from fintrack.models.core import TimestampModel, UUIDIDModel

from fintrack.models.category import SubCategory


class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"


class Transaction(UUIDIDModel, TimestampModel, table=True):
    __tablename__ = "transactions"
    type: TransactionType
    note: str | None = Field(default=None)
    sub_category: SubCategory | None = Relationship(
        back_populates="transactions")
    sub_category_id: int | None = Field(
        default=None, foreign_key="sub_categories.id")
    amount: Decimal = Field(default=0, max_digits=11, decimal_places=2)
