from decimal import Decimal

from fintrack.models.core import UUIDIDModel, TimestampModel
from sqlmodel import Field


class Account(UUIDIDModel, TimestampModel, table=True):
    __tablename__ = "accounts"
    balance: Decimal = Field(default=0, max_digits=11, decimal_places=2)
