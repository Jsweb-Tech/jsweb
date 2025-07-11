# jsweb/database.py

from sqlalchemy.orm import declarative_base, sessionmaker, relationship
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

Base = declarative_base()
SessionLocal = None
_engine = None


def init_db(database_url, echo=False, auto_create=True):
    global SessionLocal, _engine
    _engine = create_engine(database_url, echo=echo)
    SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False)
    Base.metadata.bind = _engine

    if auto_create:
        Base.metadata.create_all(_engine)


def get_engine():
    if _engine is None:
        raise RuntimeError("Database engine is not initialized. Call init_db() first.")
    return _engine


def get_session():
    if SessionLocal is None:
        raise RuntimeError("Database session is not initialized. Call init_db() first.")
    return SessionLocal()


# ✅ Custom model base class with helper methods
class ModelBase(Base):
    __abstract__ = True

    def save(self):
        db = get_session()
        db.add(self)
        db.commit()

    def delete(self):
        db = get_session()
        db.delete(self)
        db.commit()

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @classmethod
    def all(cls):
        db = get_session()
        return db.query(cls).all()

    @classmethod
    def get(cls, id):
        db = get_session()
        return db.get(cls, id)

    @classmethod
    def filter(cls, **kwargs):
        db = get_session()
        return db.query(cls).filter_by(**kwargs).all()

    @classmethod
    def first(cls, **kwargs):
        db = get_session()
        return db.query(cls).filter_by(**kwargs).first()


# ✅ Export all commonly used symbols so users import from one place
__all__ = [
    "init_db", "get_engine", "get_session", "SessionLocal", "ModelBase", "Base",
    "Integer", "String", "Float", "Boolean", "DateTime", "Text",
    "Column", "ForeignKey", "relationship"
]
