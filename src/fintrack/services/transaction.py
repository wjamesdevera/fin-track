from typing import Optional

from sqlmodel import Session, select
from fintrack.models.transaction import Transaction, TransactionType
from fintrack.models.category import SubCategory
from fintrack.services.sub_category import find_sub_category
from uuid import UUID


class InvalidAmountValue(Exception):
    pass


class InvalidTransactionType(Exception):
    pass


class SubCategoryDoesNotExist(Exception):
    pass


class TransactionNotFound(Exception):
    pass


def add_transaction(session: Session, amount: float, transaction_type: TransactionType, category: str, note: Optional[str] = None) -> Transaction:
    if type(amount) != float or amount <= 0:
        raise InvalidAmountValue
    if transaction_type not in TransactionType:
        raise InvalidTransactionType
    sub_category = find_sub_category(name=category, session=session)
    if not sub_category:
        raise SubCategoryDoesNotExist

    n_transaction = Transaction(
        amount=amount,
        type=transaction_type,
        sub_category=sub_category,
        note=note
    )
    session.add(n_transaction)
    session.commit()
    session.refresh(n_transaction)
    return n_transaction


def list_all_transactions(session: Session):
    return session.exec(select(Transaction, SubCategory).join(SubCategory, isouter=True).order_by(Transaction.created_at.desc())).all()


def find_transaction_by_id(session: Session, id: UUID) -> Transaction | None:
    return session.get(Transaction, id)


def modify_transaction(session: Session, transaction_id: UUID, amount: Optional[float] = None, transaction_type: Optional[TransactionType] = None, category: Optional[str] = None, note: Optional[str] = None) -> Transaction:
    transaction = find_transaction_by_id(session, transaction_id)
    if not transaction:
        raise TransactionNotFound
    if amount:
        if type(float(amount)) != float or amount <= 0:
            raise InvalidAmountValue
        else:
            transaction.amount = amount
    if transaction_type:
        if transaction_type not in TransactionType:
            raise InvalidTransactionType
        else:
            transaction.type = transaction_type
    if category:
        sub_category = find_sub_category(name=category, session=session)
        if not sub_category:
            raise SubCategoryDoesNotExist
        else:
            transaction.sub_category_id = sub_category.id
    if note:
        transaction.note = note

    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


def delete_transaction(session: Session, transaction_id: UUID) -> Transaction:
    transaction = find_transaction_by_id(session=session, id=transaction_id)
    if transaction is None:
        raise TransactionNotFound
    session.delete(transaction)
    return transaction
