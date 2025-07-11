
from jsweb.database import ModelBase, String, Integer, Column

# Example Model
class User(ModelBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

class User1(ModelBase):
    __tablename__ = "users2"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)