from dbgen.builder import DatabaseBuilder
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
if __name__ == '__main__':
    db = DatabaseBuilder.load_from_file('./db.yaml').build()
    user = db.tables[0]
    print(user.insert())
    engine = create_engine('postgres://postgres:postgres@localhost/demo')
    print(CreateTable(user).compile(engine))
