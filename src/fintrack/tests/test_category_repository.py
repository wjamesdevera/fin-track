import pytest
from fintrack.repositories.category_repository import CategoryRepository
from fintrack.db import test_engine
from fintrack.seeds.seed import seed_all
from sqlmodel import SQLModel, Session


@pytest.fixture
def repo():
    return CategoryRepository()


@pytest.fixture
def setup_test_db(monkeypatch):
    """Create test database tables and patch the engine for testing."""
    # Create all tables
    SQLModel.metadata.create_all(test_engine)
    seed_all(session=Session(test_engine))

    # Patch the engine used by CategoryRepository
    monkeypatch.setattr(
        'fintrack.repositories.category_repository.engine', test_engine)

    yield

    # Cleanup: drop all tables after test
    SQLModel.metadata.drop_all(test_engine)


def test_add_category(setup_test_db, repo):
    """Test adding a new category."""
    result = repo.add("New Category")

    # Verify the object was returned
    assert result is not None

    # Verify it was actually added by finding it in the database
    found = repo.find_by_name("New Category")
    assert found is not None
    assert found.name == "New Category"


def test_add_existing_category(setup_test_db, repo):
    """Test adding an existing category"""

    with pytest.raises(Exception):
        result = repo.add("expense")


def test_changing_name_of_category(setup_test_db, repo):
    """Test changing name of category"""
    result = repo.change_name("expense", "Expense")

    assert result is not None

    found = repo.find_by_name("Expense")
    assert found is not None
    assert found.name == "Expense"
