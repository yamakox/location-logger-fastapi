from sqlmodel import SQLModel, Session, select
from .model import Client, Location
import typer
from rich import print

from .engine import engine

# MARK: CLI

app = typer.Typer(add_completion=False)
app_clients = typer.Typer(add_completion=False)
app_locations = typer.Typer(add_completion=False)


@app.command()
def init():
    """データベースに接続して、テーブルを初期化します。"""
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


@app_clients.command(name='list')
def clients_list():
    """クライアントを一覧表示します。"""
    with Session(engine) as session:
        statement = select(Client)
        results = session.exec(statement)
        for row in results:
            print(row)


@app_locations.command(name='list')
def locations_list():
    """位置情報を一覧表示します。"""
    with Session(engine) as session:
        statement = select(Location)
        results = session.exec(statement)
        for row in results:
            print(row)


app.add_typer(app_clients, name='clients', help='クライアントに関するコマンドセットです。')
app.add_typer(app_locations, name='locations', help='位置情報に関するコマンドセットです。')

if __name__ == '__main__':
    app()
