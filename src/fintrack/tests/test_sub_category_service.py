import pytest
from fintrack.db import test_engine
from fintrack.seeds.seed import seed_all
from sqlmodel import SQLModel, Session, select
from fintrack.services.sub_category import add_sub_category, list_all_sub_category
from fintrack.models.category import Category, SubCategory


@pytest.fixture
def session():
    db_session = Session(test_engine)
    try:
        yield db_session
    finally:
        db_session.close()


@pytest.fixture
def setup_test_db():
    """Create test database tables and patch the engine for testing."""
    # Create all tables
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        seed_all(session)
    yield Session(test_engine)

    # Cleanup: drop all tables after test
    SQLModel.metadata.drop_all(test_engine)


def test_add_sub_category(setup_test_db, session) -> None:
    """Test adding sub category"""
    NEW_SUB_CATEGORY_NAME = "test_subcategory"
    category = session.exec(select(Category).where(
        Category.id == 1)).one_or_none()
    new_sc = add_sub_category(
        category=category,
        name=NEW_SUB_CATEGORY_NAME,
        session=session
    )

    assert new_sc is not None

    found = session.exec(select(SubCategory).where(
        SubCategory.name == NEW_SUB_CATEGORY_NAME)).one_or_none()

    assert found is not None
    assert found.category_id == 1
    assert found.name == NEW_SUB_CATEGORY_NAME


def test_add_existing_sub_category(setup_test_db, session) -> None:
    """Test adding existing sub category"""
    existing_subcategory = session.exec(
        select(SubCategory).where(SubCategory.id == 1)).one_or_none()
    category = session.exec(select(Category).where(
        Category.id == 1)).one_or_none()

    with pytest.raises(Exception):
        new_sc = add_sub_category(
            category=category,
            name=existing_subcategory.name,
            session=session
        )


def test_list_all_sub_category(setup_test_db, session) -> None:
    """Test list all sub category"""
    sub_categories = list_all_sub_category(session=session)

    assert sub_categories is not None
    assert len(sub_categories) > 0
