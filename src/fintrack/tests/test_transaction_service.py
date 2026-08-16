import pytest
from sqlmodel import Session, SQLModel, select
from fintrack.db import test_engine
from fintrack.services.transaction import add_transaction, list_all_transaction
from fintrack.models.transaction import Transaction, TransactionType
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


def test_list_all_transactions(setup_test_db, session):
    test_category_1 = Category(name="expense")
    test_subcategory_1 = SubCategory(
        name="transportation", category=test_category_1)
    test_transaction_1 = Transaction(
        amount=500.5,
        type=TransactionType.EXPENSE,
        sub_category=test_subcategory_1,
        note="Grab"
    )

    test_transaction_2 = Transaction(
        amount=20,
        type=TransactionType.EXPENSE,
        sub_category=test_subcategory_1,
        note="Jeepney"
    )
    session.add(test_category_1)
    session.add(test_subcategory_1)
    session.add_all(
        [test_category_1, test_subcategory_1,
            test_transaction_1, test_transaction_2]
    )
    session.commit()

    transactions = list_all_transaction(session)

    assert len(transactions) == 2
    # Checks if order is in desc order by creation
    assert transactions[0].note == "Jeepney"
    assert transactions[1].note == "Grab"
