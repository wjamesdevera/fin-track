import click
from fintrack.db import engine
from sqlmodel import Session
from fintrack.models.category import SubCategory
from fintrack.services.transaction import list_all_transactions
from fintrack.services.sub_category import list_all_sub_category
from fintrack.models.transaction import Transaction

TABLE_HEADERS = [
    "date",
    "id",
    "type",
    "category",
    "amount",
    "note"
]


def _blank_if_none(s: str | None):
    return "" if s is None else s


def _format_transaction(row: tuple[Transaction, SubCategory]) -> str:
    transaction, subcategory = row
    date: str = transaction.created_at.strftime("%Y-%m-%d")
    id: str = transaction.id.hex
    return f'{date:>20}|{id:>30}|{transaction.type.title():>20}|{subcategory.name.title():>20}|{transaction.amount:>20.2f}|{_blank_if_none(transaction.note):>20}'


@click.command(name="list", epilog="Examples:\n\n\b\n  fintrack list\n")
@click.argument("category")
def list(category):
    if category == "transactions":
        with Session(engine) as session:
            transactions = list_all_transactions(session=session)
        if not transactions:
            print("No Transactions Found")
        header = "|".join([f"{header:>20}" if header !=
                           "id" else f'{header:>32}' for header in TABLE_HEADERS])
        print(header)
        for transaction in transactions:
            print(_format_transaction(transaction))
    if category == "category":
        with Session(engine) as session:
            subcategories = list_all_sub_category(session)
        for sc in subcategories:
            print(f'{sc.name}')
