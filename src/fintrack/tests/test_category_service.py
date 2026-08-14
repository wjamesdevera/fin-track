import pytest
from fintrack.db import test_engine
from fintrack.seeds.seed import seed_all
from sqlmodel import SQLModel, Session, select
from fintrack.services.category import add_category, update_category, delete_category, find_category
from fintrack.models.category import Category


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


def test_add_category(setup_test_db, session):
    """Test adding a new category."""
    NEW_CATEGORY_NAME = "New Category"
    result = add_category(NEW_CATEGORY_NAME, session=session)

    # Verify the object was returned
    assert result is not None

    # Verify it was actually added by finding it in the database
    found = session.exec(select(Category).where(
        Category.name == NEW_CATEGORY_NAME)).one_or_none()
    assert found is not None
    assert found.name == NEW_CATEGORY_NAME


def test_add_existing_category(setup_test_db, session):
    """Test adding an existing category"""
    with pytest.raises(Exception):
        add_category("expense", session=session)


def test_changing_name_of_category(setup_test_db, session):
    """Test changing name of category"""
    OLD_CATEGORY_NAME = "expense"
    NEW_CATEGORY_NAME = "EXPENSE"
    result = update_category(
        OLD_CATEGORY_NAME, NEW_CATEGORY_NAME, session=session)

    assert result is not None

    found = session.exec(select(Category).where(
        Category.name == NEW_CATEGORY_NAME)).one_or_none()
    assert found is not None
    assert found.name == NEW_CATEGORY_NAME


def test_changing_name_for_non_existing_category(setup_test_db, session):
    """Test changing name for non-existing category"""
    OLD_CATEGORY_NAME = "New Category"
    NEW_CATEGORY_NAME = "EXPENSE"
    with pytest.raises(Exception):
        result = update_category(
            OLD_CATEGORY_NAME, NEW_CATEGORY_NAME, session=session)


def test_deleting_category(setup_test_db, session):
    """Test deleting a category"""
    CATEGORY_NAME_TO_DELETE = "expense"
    deleted = delete_category(CATEGORY_NAME_TO_DELETE, session=session)

    assert deleted is not None

    found = session.exec(select(Category).where(
        Category.name == CATEGORY_NAME_TO_DELETE)).one_or_none()
    assert found is None
