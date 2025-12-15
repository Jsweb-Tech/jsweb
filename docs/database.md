# Database

JsWeb provides a simple and powerful way to work with databases using [SQLAlchemy](https://www.sqlalchemy.org/), a popular SQL toolkit and Object-Relational Mapper (ORM).

## Configuration

To get started, you need to configure your database connection in your `config.py` file.

```python
# config.py
SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## Defining Models

Models are Python classes that represent the tables in your database. You can define your models in the `models.py` file by inheriting from `jsweb.database.ModelBase`.

```python
# models.py
from jsweb.database import ModelBase, Column, Integer, String

class User(ModelBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
```

## Database Migrations

JsWeb uses [Alembic](https://alembic.sqlalchemy.org/) to handle database migrations. Alembic allows you to track changes to your database schema and apply them in a systematic way.

### Generating a Migration

To generate a new migration script, you can use the `jsweb db prepare` command.

```bash
jsweb db prepare -m "Create user table"
```

This will create a new migration file in the `alembic/versions` directory.

### Applying a Migration

To apply the migration to your database, you can use the `jsweb db upgrade` command.

```bash
jsweb db upgrade
```

This will run the migration script and create the `user` table in your database.

## Querying the Database

You can use SQLAlchemy to query the database in your views.

```python
from .models import User

@app.route("/users")
async def user_list(req):
    users = User.query.all()
    return render(req, "users.html", {"users": users})
```

### Creating a New User

The `ModelBase` class provides a `create` method that creates and saves a new model instance in a single step.

```python
from .models import User

new_user = User.create(username="john", email="john@example.com")
```

### Getting a User by ID

```python
user = User.query.get(1)
```

### Filtering Users

```python
users = User.query.filter_by(username="john").all()
```
