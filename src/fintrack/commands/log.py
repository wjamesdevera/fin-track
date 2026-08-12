import click
from sqlmodel import Session, select
from ..models.models import Transaction, SubCategory, TransactionType
from ..db import engine


@click.command(name="log")
@click.option("-a", "--amount", type=float, help="Transaction Amount")
@click.option("-t", "--type", type=str, default="expense", help="expense/income")
@click.option("-c", "--category", type=str)
@click.option("-n", "--note", type=str, default=None)
def log(amount: float, type: str, category: str, note: str | None) -> None:
    with Session(engine) as session:
        statement = select(SubCategory).where(
            SubCategory.name == category)
        obj_category = session.exec(statement).first()

        if not obj_category:
            raise ValueError("Category not found")

        new_type = TransactionType.EXPENSE if type.lower(
        ) == "expense" else TransactionType.INCOME

        new_transaction = Transaction(
            amount=amount, type=new_type, sub_category_id=obj_category.id, note=note)

        session.add(new_transaction)
        session.commit()

        click.echo(
            f'Added: amount: ${amount} | type: {new_type.lower()} | category: {obj_category.name} | note: {note}')
