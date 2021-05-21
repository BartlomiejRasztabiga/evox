from sqlalchemy.orm import Session


def test_test(db: Session) -> None:
    assert True is True
