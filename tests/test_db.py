from sqlalchemy import text, Integer
from sqlalchemy.orm import Mapped, mapped_column
import pytest
from app.db.base import Base, get_db

def test_database_connection():
    """Test database connection"""
    db = next(get_db())
    result = db.execute(text("SELECT 1")).scalar()
    assert result == 1

def test_get_db():
    """Test get_db dependency"""
    db = next(get_db())
    assert db is not None
    db.close()

def test_base_class():
    """Test SQLAlchemy Base class configuration"""
    # Test table naming convention
    class TestModel(Base):
        __tablename__ = "test_model"
        id: Mapped[int] = mapped_column(Integer, primary_key=True)

    assert hasattr(TestModel, "__table__")
    assert TestModel.__table__.name == "test_model"

def test_session_rollback():
    """Test session rollback on error"""
    db = next(get_db())
    try:
        # Execute invalid SQL to trigger an error
        with pytest.raises(Exception):
            db.execute(text("SELECT * FROM nonexistent_table"))
            db.commit()

        # Verify session is still usable after rollback
        db.rollback()
        result = db.execute(text("SELECT 1")).scalar()
        assert result == 1
    finally:
        db.close()
