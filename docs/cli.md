# Command-Line Interface

JsWeb comes with a powerful command-line interface (CLI) that helps you manage your application. You can use the CLI to create new projects, run the development server, manage database migrations, and more.

## `jsweb run`

This command starts the development server.

```bash
jsweb run
```

### Options

*   `--host`: The host to bind to. Defaults to `127.0.0.1`.
*   `--port`: The port to listen on. Defaults to `8000`.
*   `--reload`: Enable auto-reloading. The server will restart whenever you make changes to your code.
*   `--qr`: Display a QR code for accessing the server on your local network.

## `jsweb new`

This command creates a new JsWeb project with a standard directory structure.

```bash
jsweb new myproject
```

This will create a `myproject` directory with all the necessary files to get you started.

## `jsweb db`

This command is used to manage your database migrations with Alembic.

### `jsweb db prepare`

This command generates a new migration script based on the changes to your models.

```bash
jsweb db prepare -m "A short message describing the changes"
```

### `jsweb db upgrade`

This command applies all pending migrations to the database.

```bash
jsweb db upgrade
```

### `jsweb db downgrade`

This command reverts the last applied migration.

```bash
jsweb db downgrade
```

## `jsweb create-admin`

This command creates a new admin user for the built-in admin interface.

```bash
jsweb create-admin
```

You will be prompted to enter a username, email, and password for the new admin user.
