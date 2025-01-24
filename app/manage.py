import typer
from app.interface.cli.auth import app as auth_app

app = typer.Typer()

app.add_typer(auth_app, name="auth")

@app.command()
def version():
    print("v0.0.1")


if __name__ == "__main__":
    app()
