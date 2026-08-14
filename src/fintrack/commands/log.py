import click
from sqlmodel import Session, select
from ..models.category import Transaction, SubCategory, TransactionType
from ..db import engine


@click.command(name="log", epilog="Examples:\n\n\b\n  fintrack log --amount 45.50 --type expense --category \"Food\" --note \"Lunch with team\"\n")
@click.option("-a", "--amount", type=float, help="Transaction Amount")
@click.option("-t", "--type", type=str, default="expense", help="expense/income")
@click.option("-c", "--category", type=str)
@click.option("-n", "--note", type=str, default=None)
def log(amount: float, type: str, category: str, note: str | None) -> None:
    """A command use to log a transaction and store into local db"""
    with Session(engine) as session:
        # checks if category is in sub categories in database
        statement = select(SubCategory).where(
            SubCategory.name == category)
        obj_category = session.exec(statement).first()

        if not obj_category:
            raise click.BadParameter(
                f"{category} does not exist")

        if type.lower() not in TransactionType:
            raise click.BadParameter("Transaction type not valid")

        new_type = TransactionType.EXPENSE if type.lower(
        ) == "expense" else TransactionType.INCOME

        # checks if amount is negative
        if amount <= 0:
            raise click.BadParameter("Amount could not be a negative or 0")

        # creates a new transaction
        new_transaction = Transaction(
            amount=amount, type=new_type, sub_category_id=obj_category.id, note=note)
        session.add(new_transaction)

        session.commit()

        click.echo(
            f'Added: amount=${amount} | type={new_type.lower()} | category={obj_category.name} | note={note}')
