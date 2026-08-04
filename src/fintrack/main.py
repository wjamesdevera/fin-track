import click
from .db import engine, SQLModel
from .seeds.seed import seed_all


@click.command()
def cli():
    """Prints a greeting"""
    click.echo("Hello, World!")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def start_app():
    create_db_and_tables()
    seed_all()
    cli()
