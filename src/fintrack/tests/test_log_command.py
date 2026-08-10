from fintrack.commands.log import log


def test_log_valid() -> None:
    log(45.50, "expense", "Food", "Lunch with team")


def test_log_amount_valid() -> None:
    log(45.50, "expense", "Food", "Lunch with team")


def test_log_amount_invalid() -> None:
    log("food", "expense", "Food", "Lunch with team")


def test_log_type_valid() -> None:
    pass


def test_log_type_invalid() -> None:
    pass


def test_log_category_valid() -> None:
    pass


def test_log_category_invalid() -> None:
    pass


def test_log_note_valid() -> None:
    pass


def test_log_note_invalid() -> None:
    pass
