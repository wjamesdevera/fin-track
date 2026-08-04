from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime, timezone


class SimpleIDModel(SQLModel):
    id: int | None = Field(primary_key=True)


class UUIDIDModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class TimestampModel(SQLModel):
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)

    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={
            "onupdate": lambda:
                datetime.now(timezone.utc)
        }
    )


class EventTimestampModel(SQLModel):
    occured_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)

    )
