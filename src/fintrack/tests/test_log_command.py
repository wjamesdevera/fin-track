from fintrack.commands.log import log
from fintrack.models.models import SubCategory, TransactionType
from click.testing import CliRunner
import pytest


class DummyQueryResult:
    def __init__(self, category):
        self._category = category

    def first(self):
        return self._category


class DummySession:
    def __init__(self, engine=None):
        self.added = None
        self.committed = False
        self.category = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def exec(self, statement):
        return DummyQueryResult(self.category)

    def add(self, transaction):
        self.added = transaction

    def commit(self):
        self.committed = True


@pytest.fixture
def runner():
    """Fixture to provide a standard CliRunner instance."""
    return CliRunner()


def test_log_valid(runner, monkeypatch) -> None:
    session = DummySession()
    session.category = SubCategory(id=1, name='Groceries')

    monkeypatch.setattr('fintrack.commands.log.Session',
                        lambda engine: session)

    result = runner.invoke(log, [
        '--amount', '45.50',
        '--type', 'expense',
        '--category', 'Groceries',
        '--note', 'Lunch with team'
    ])

    assert result.exit_code == 0
    assert 'Added: amount: $45.5 | type: expense | category: Groceries | note: Lunch with team' in result.output
    assert session.added is not None
    assert session.committed is True
    assert session.added.type == TransactionType.EXPENSE
    assert float(session.added.amount) == 45.50
    assert session.added.sub_category_id == 1
    assert session.added.note == 'Lunch with team'


def test_log_amount_invalid_type(runner, monkeypatch) -> None:
    session = DummySession()
    session.category = SubCategory(id=1, name='Groceries')

    monkeypatch.setattr('fintrack.commands.log.Session',
                        lambda engine: session)

    result = runner.invoke(log, [
        '--amount', 'somestring',
        '--type', 'expense',
        '--category', 'Groceries',
        '--note', 'Lunch with team'
    ])

    assert result.exit_code != 0
    assert session.added is None
    assert session.committed is False


def test_log_amount_negative_amount(runner, monkeypatch) -> None:
    session = DummySession()
    session.category = SubCategory(id=1, name='Groceries')

    monkeypatch.setattr('fintrack.commands.log.Session',
                        lambda engine: session)

    result = runner.invoke(log, [
        '--amount', '-45.50',
        '--type', 'expense',
        '--category', 'Groceries',
        '--note', 'Lunch with team'
    ])

    assert result.exit_code != 0
    assert session.added is None
    assert session.committed is False


def test_log_type_invalid(runner, monkeypatch) -> None:
    session = DummySession()
    session.category = SubCategory(id=1, name='Groceries')

    monkeypatch.setattr('fintrack.commands.log.Session',
                        lambda engine: session)

    result = runner.invoke(log, [
        '--amount', '45.50',
        '--type', 'savings',
        '--category', 'Groceries',
        '--note', 'Lunch with team'
    ])

    assert result.exit_code != 0
    assert session.added is None
    assert session.committed is False


def test_log_category_invalid(runner, monkeypatch) -> None:
    session = DummySession()
    session.category = SubCategory(id=1, name='Groceries')

    monkeypatch.setattr('fintrack.commands.log.Session',
                        lambda engine: session)

    result = runner.invoke(log, [
        '--amount', '45.50',
        '--type', 'expense',
        '--category', 'Not in the category',
        '--note', 'Lunch with team'
    ])

    assert result.exit_code != 0
    assert session.added is None
    assert session.committed is False


def test_log_note_optional(runner, monkeypatch) -> None:
    session = DummySession()
    session.category = SubCategory(id=1, name='Groceries')

    monkeypatch.setattr('fintrack.commands.log.Session',
                        lambda engine: session)

    result = runner.invoke(log, [
        '--amount', '45.50',
        '--type', 'expense',
        '--category', 'Groceries'
    ])

    assert result.exit_code == 0
    assert session.added is not None
    assert session.committed is True
    assert session.added.type == TransactionType.EXPENSE
    assert float(session.added.amount) == 45.50
    assert session.added.sub_category_id == 1
