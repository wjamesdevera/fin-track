from sqlmodel import Session, select


def exists(session: Session, model, name: str) -> bool:
    statement = select(model).where(model.name == name)
    return session.exec(statement).first() is not None
