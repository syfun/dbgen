from dbgen.builder import DatabaseBuilder
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable


if __name__ == '__main__':
    builder = DatabaseBuilder.load_from_file('./db.yaml')
    db = builder.build()
    user = db.tables[0]
    print(user.insert())
    engine = create_engine(builder.url)
    print(CreateTable(user).compile(engine))
