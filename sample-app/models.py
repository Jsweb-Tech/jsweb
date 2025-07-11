from jsweb.database import ModelBase, String, Integer, Column


# Example Model
class User(ModelBase):
    __tablename__ = 'users'  # Explicit table name is good practice
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)


class User1(ModelBase):
    __tablename__ = 'users1'  # Explicit table name is good practice
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    name1 = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
