import pytest
from sqlmodel import Session, SQLModel, select
from fintrack.db import test_engine
from fintrack.services.transaction import add_transaction, find_transaction_by_id, list_all_transactions, modify_transaction, delete_transaction
from fintrack.models.transaction import Transaction, TransactionType
from fintrack.models.category import Category, SubCategory
import uuid


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


def _seed_test_categories(session: Session) -> tuple[Category, SubCategory]:
    test_category_1 = Category(name="expense")
    test_subcategory_1 = SubCategory(
        name="transportation", category=test_category_1)
    session.add_all([test_category_1, test_subcategory_1])
    session.commit()
    session.refresh(test_category_1)
    session.refresh(test_subcategory_1)
    return test_category_1, test_subcategory_1


def _seed_test_transactions(session: Session) -> tuple[Transaction, Transaction]:
    test_category_1, test_subcategory_1 = _seed_test_categories(session)
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
        [test_transaction_1, test_transaction_2]
    )
    session.commit()
    session.refresh(test_transaction_1)
    session.refresh(test_transaction_2)
    return test_transaction_1, test_transaction_1


def test_add_transaction(setup_test_db, session):
    """Test adding a valid transaction"""
    _seed_test_categories(session)

    new_transaction = add_transaction(
        session=session,
        amount=500.50,
        transaction_type="expense",
        category="transportation",
        note="Grab ride"
    )

    transactions = session.exec(select(Transaction)).all()

    assert len(transactions) != 0
    assert transactions[0].amount == new_transaction.amount
    assert transactions[0].type == new_transaction.type
    assert transactions[0].sub_category_id == new_transaction.sub_category_id
    assert transactions[0].note == new_transaction.note


def test_list_all_transactions(setup_test_db, session):

    _seed_test_transactions(session)
    transactions = list_all_transactions(session)

    assert len(transactions) == 2
    # Checks if order is in desc order by creation
    assert transactions[0].note == "Jeepney"
    assert transactions[1].note == "Grab"


def test_find_transaction_by_id(setup_test_db, session):
    test_transaction_1 = _seed_test_transactions(session)

    transaction = find_transaction_by_id(session, test_transaction_1.id)

    assert transaction is not None
    assert transaction.id == test_transaction_1.id


def test_find_transaction_by_id(setup_test_db, session):
    _seed_test_transactions(session)

    transaction = find_transaction_by_id(session, uuid.uuid4())

    assert transaction is None


def test_modify_transaction(setup_test_db, session):
    category = session.exec(select(Category)).first()
    test_sub_category = SubCategory(name="new category", category=category)

    session.add(test_sub_category)
    session.commit()
    session.refresh(test_sub_category)
    test_transaction_1, test_transaction_2 = _seed_test_transactions(session)

    # test modifying all fields
    transaction = modify_transaction(
        session,
        transaction_id=test_transaction_2.id,
        amount=1000,
        transaction_type="income",
        category=test_sub_category.name,
        note="modified note"
    )

    assert transaction is not None
    assert transaction.id == test_transaction_2.id
    assert transaction.amount == 1000
    assert transaction.type == "income"
    assert transaction.sub_category == test_sub_category
    assert transaction.note == "modified note"

    # test modifying amount
    transaction = modify_transaction(
        session,
        transaction_id=test_transaction_1.id,
        amount=float(20)
    )

    assert transaction is not None
    assert transaction.id == test_transaction_1.id
    assert transaction.amount == 20.0

    # test modifying transaction type
    transaction = modify_transaction(
        session,
        transaction_id=test_transaction_1.id,
        transaction_type="income"
    )

    assert transaction is not None
    assert transaction.id == test_transaction_1.id
    assert transaction.type == "income"

    # test modifying category
    transaction = modify_transaction(
        session,
        transaction_id=test_transaction_1.id,
        category=test_sub_category.name
    )

    assert transaction is not None
    assert transaction.id == test_transaction_1.id
    assert transaction.sub_category == test_sub_category

    # test modifying note
    transaction = modify_transaction(
        session,
        transaction_id=test_transaction_1.id,
        note="modified note"
    )

    assert transaction is not None
    assert transaction.id == test_transaction_1.id
    assert transaction.note == "modified note"


def test_delete_transaction(setup_test_db, session):
    test_transaction_1, test_transaction_2 = _seed_test_transactions(session)

    deleted_transaction = delete_transaction(
        session=session, transaction_id=test_transaction_1.id)
    transactions = session.exec(select(Transaction)).fetchall()

    assert deleted_transaction is not None
    assert len(transactions) < 2
