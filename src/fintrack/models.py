from sqlmodel import Field, SQLModel, Relationship


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str

    sub_categories: list["SubCategories"] = Relationship(
        back_populates="sub_categories")


class SubCategories(SQLModel, table=True):
    __tablename__ = "sub_categories"
    id: int | None = Field(default=None, primary_key=True)
    name: str

    category_id: int | None = Field(default=None, foreign_key="categories.id")
    category: Category | None = Relationship(back_populates="categories")
