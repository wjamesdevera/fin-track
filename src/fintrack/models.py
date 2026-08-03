from typing import Optional
import uuid
from decimal import Decimal
from datetime import datetime, timezone
from time import timezone
from sqlmodel import Field, SQLModel, Relationship


class SimpleIDModel(SQLModel):
    id: int | None = Field(primary_key=True)


class UUIDIDModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class TimestampaModel(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)

    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={
            "onupdate": lambda:
                datetime.now(timezone.utc)
        }
    )


class EventTimestampModel(SQLModel):
    occured_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)

    )


class Category(SimpleIDModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str

    sub_categories: list["SubCategory"] = Relationship(
        back_populates="sub_categories")


class SubCategory(SimpleIDModel, table=True):
    __tablename__ = "sub_categories"
    name: str

    category_id: int | None = Field(default=None, foreign_key="categories.id")
    category: Category | None = Relationship(back_populates="categories")


class Transaction(UUIDIDModel, TimestampaModel, table=True):
    __tablename__ = "transactions"
    amount: Decimal = Field(default=0, max_digits=11, decimal_places=2)
