import typer

app = typer.Typer()


@app.command()
def version():
    print("v0.0.1")


if __name__ == "__main__":
    app()
