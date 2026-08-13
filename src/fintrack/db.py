from sqlmodel import create_engine, SQLModel
from sqlmodel.pool import StaticPool


sqlite_file_name = "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

test_sqlite_file_name = "data/testing.db"
test_sqlite_url = f"sqlite:///{test_sqlite_file_name}"
test_engine = create_engine(test_sqlite_url,
                            connect_args={"check_same_thread": False},
                            poolclass=StaticPool)
