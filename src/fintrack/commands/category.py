import click
from sqlmodel import Session, select
from fintrack.services.sub_category import add_sub_category, list_all_sub_category, delete_sub_category
from fintrack.models.category import Category
from fintrack.db import engine


@click.group()
def category():
    pass


@category.command(name="add")
@click.argument("name")
def add(name: str):
    with Session(engine) as session:
        category = session.exec(select(Category)).first()
        add_sub_category(session=session, category=category, name=name)


@category.command(name="list")
def list():
    with Session(engine) as session:
        categories = list_all_sub_category(session=session)
        print("Printing Categories...")
        for category in categories:
            print(f"{category.id}: {category.name.title()}")


@category.command(name="delete")
@click.argument("name")
def delete(name: str):
    with Session(engine) as session:
        if delete_sub_category(session=session, identifier=name):
            print(f"Deleted: Subcategory={name}")
