import click
from .db import engine, SQLModel
from .commands.log import log
from .seeds.seed import seed_all

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
WELCOME_MESSGAGE = """
Fintrack [version 1.0.0]

Usage:  fintrack [options]

FinTrack is a lightweight CLI tool for rapid expense and income tracking. 
Built for terminal users, it eliminates logging friction by replacing bulky 
apps and spreadsheets with a seamless, high-velocity workflow.
"""


@click.group()
def main():
    pass


@main.command(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Fintrack [version 1.0.0]

    FinTrack is a lightweight CLI tool for rapid expense and income tracking. Built for terminal users, it eliminates logging friction by replacing bulky apps and spreadsheets with a seamless, high-velocity workflow.
    """
    click.echo(WELCOME_MESSGAGE)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def start_app():
    create_db_and_tables()
    seed_all()
    main()


main.add_command(log)
