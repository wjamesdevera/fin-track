from ..models.models import Category, SubCategory
from sqlmodel import Session, select
from .seed_utils import exists

categories = [
    {
        "name": "expense",
        "sub_categories": [
            {"name": "Food & Dining"},
            {"name": "Groceries"},
            {"name": "Housing & Rent"},
            {"name": "Utilities"},
            {"name": "Transportation"},
            {"name": "Entertainment"},
            {"name": "Shopping"},
            {"name": "Healthcare & Medical"},
            {"name": "Subscriptions & Services"},
            {"name": "Personal Care"},
            {"name": "Travel & Vacation"},
            {"name": "Education & Learning"},
            {"name": "Pets"},
            {"name": "Gifts & Donations"}
        ]
    },
    {
        "name": "income",
        "sub_categories": [
            {"name": "Salary / Wages"},
            {"name": "Freelance / Side Hustle"},
            {"name": "Investments & Dividends"},
            {"name": "Rental Income"},
            {"name": "Gifts & Grants"},
            {"name": "Refunds & Cashbacks"},
            {"name": "Other Income"}
        ]
    },
    {
        "name": "savings_and_investments",
        "sub_categories": [
            {"name": "Emergency Fund"},
            {"name": "Retirement (401k / IRA)"},
            {"name": "Stocks & ETFs"},
            {"name": "Crypto"},
            {"name": "Real Estate"}
        ]
    },
    {
        "name": "debt_and_loans",
        "sub_categories": [
            {"name": "Credit Card Payment"},
            {"name": "Student Loan"},
            {"name": "Auto Loan"},
            {"name": "Mortgage"},
            {"name": "Personal Loan"}
        ]
    },
    {
        "name": "transfer",
        "sub_categories": [
            {"name": "Account to Account"},
            {"name": "Credit Card Settlement"},
            {"name": "ATM Withdrawal"}
        ]
    }
]


def _seed_categories(session: Session):
    for category in categories:
        if not exists(session, Category, category["name"]):
            session.add(Category(name=category["name"]))
    session.commit()


def _seed_subcategories(session: Session):
    for category in categories:
        category_o = session.exec(
            select(Category).where(Category.name == category["name"])
        ).first()
        if category_o is None:
            continue  # category wasn't found/seeded, skip its sub-categories

        for sub_category in category["sub_categories"]:
            if not exists(session, SubCategory, sub_category["name"]):
                session.add(
                    SubCategory(
                        name=sub_category["name"], category_id=category_o.id)
                )
    session.commit()


def seed(session: Session):
    _seed_categories(session)
    _seed_subcategories(session)
