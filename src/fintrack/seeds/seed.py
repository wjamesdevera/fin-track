from .seed_category import seed as seed_categories
from ..db import engine
from sqlmodel import Session


def seed_all():
    with Session(engine) as session:
        seed_categories(session)
