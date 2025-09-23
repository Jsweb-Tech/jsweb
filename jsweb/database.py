# jsweb/database.py

from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Create a session factory. This is not yet bound to an engine.
Session = sessionmaker(expire_on_commit=False)
# Create a thread-local session object. This is the object that should be used in the app.
db_session = scoped_session(Session)

# Create a declarative base and add a query property to it.
# This allows for `MyModel.query.filter_by(...)` syntax.
Base = declarative_base()
Base.query = db_session.query_property()

_engine = None

def init_db(database_url, echo=False):
    """Initializes the database engine and configures the session factory."""
    global _engine
    _engine = create_engine(database_url, echo=echo)
    Session.configure(bind=_engine)
    Base.metadata.bind = _engine

def get_engine():
    """Returns the database engine instance."""
    if _engine is None:
        raise RuntimeError("Database engine is not initialized. Call init_db() first.")
    return _engine

class DatabaseError(Exception):
    """Custom exception for database operations."""
    pass

def _handle_db_error(e):
    """Rolls back the session and raises a custom DatabaseError."""
    db_session.rollback()
    if isinstance(e, IntegrityError):
        simple_message = str(e.orig)
        raise DatabaseError(f"Constraint failed: {simple_message}") from e
    else:
        raise DatabaseError(f"Database operation failed: {e}") from e

class ModelBase(Base):
    """
    An abstract base model that provides convenience methods for database operations.
    """
    __abstract__ = True

    @classmethod
    def create(cls, **kwargs):
        """Create and save a new model instance in a single step."""
        instance = cls(**kwargs)
        instance.save()
        return instance

    def update(self, **kwargs):
        """Update attributes of the model instance and save the changes."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def save(self):
        """Saves the object, handling potential errors and transaction rollback."""
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError as e:
            _handle_db_error(e)

    def delete(self):
        """Deletes the object, handling potential errors and transaction rollback."""
        try:
            db_session.delete(self)
            db_session.commit()
        except SQLAlchemyError as e:
            _handle_db_error(e)

    def to_dict(self):
        """Returns a dictionary representation of the model's columns."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

__all__ = [
    "init_db", "get_engine", "db_session", "ModelBase", "Base",
    "DatabaseError",
    "Integer", "String", "Float", "Boolean", "DateTime", "Text",
    "Column", "ForeignKey", "relationship"
]
