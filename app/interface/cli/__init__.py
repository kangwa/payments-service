import typer

from .auth import app as auth_app

app = typer.Typer()

app.add_typer(auth_app)