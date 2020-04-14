import click
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable, CreateSchema

from dbgen.builder import DatabaseBuilder


@click.group()
def main():
    pass


@main.command()
@click.option('-f', '--file', help='db yaml config')
def printsql(file):
    def dump(sql, *multiparams, **params):
        print(sql.compile(dialect=engine.dialect))

    builder = DatabaseBuilder.load_from_file(file)
    db = builder.build()
    engine = create_engine(builder.url, strategy='mock', executor=dump)
    db.metadata.create_all(engine, checkfirst=False)
