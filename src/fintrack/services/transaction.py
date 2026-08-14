from typing import Optional

from sqlmodel import Session
from fintrack.db import engine
from fintrack.models.transaction import Transaction, TransactionType
from fintrack.services.sub_category import find_sub_category


class InvalidAmountValue(Exception):
    pass


class InvalidTransactionType(Exception):
    pass


class SubCategoryDoesNotExist(Exception):
    pass


def add_transaction(session: Session, amount: float, transaction_type: TransactionType, category: str, note: Optional[str] = None):
    if type(amount) != float or amount <= 0:
        raise InvalidAmountValue
    if transaction_type not in TransactionType:
        raise InvalidTransactionType
    with Session(engine) as session:
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
