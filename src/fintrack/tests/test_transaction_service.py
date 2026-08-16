import pytest
from sqlmodel import Session, SQLModel, select
from fintrack.db import test_engine
from fintrack.seeds.seed import seed_all
from fintrack.services.transaction import add_transaction
from fintrack.models.transaction import Transaction
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

    yield

    # Cleanup: drop all tables after test
    SQLModel.metadata.drop_all(test_engine)


def test_add_transaction(setup_test_db, session):
    """Test adding a valid transaction"""
    test_category_1 = Category(name="expense")
    test_subcategory_1 = SubCategory(
        name="transportation", category=test_category_1)
    session.add(test_category_1)
    session.add(test_subcategory_1)
    session.commit()

    new_transaction = add_transaction(
        session=session,
        amount=500.50,
        transaction_type="expense",
        category="transportation",
        note="Grab ride"
    )

    transactions = session.exec(select(Transaction)).all()

    assert len(transactions) != 0
