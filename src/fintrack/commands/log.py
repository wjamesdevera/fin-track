import click
from sqlmodel import Session
from ..models.models import Transaction
from ..db import engine


@click.command(name="log")
@click.option("-a", "--amount", type=float, help="Transaction Amount")
@click.option("-t", "--type", type=str, default="expense", help="expense/income")
@click.option("-c", "--category", type=str)
@click.option("-n", "--note", type=str, default=None)
def log(amount: float, type: str, category: str, note: str | None) -> None:

    click.echo(
        f'amount: {amount} | type: {type} | category: {category} | note: {note}')
