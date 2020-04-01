from alembic.runtime.migration import MigrationContext
from alembic.autogenerate import compare_metadata, produce_migrations
from sqlalchemy.schema import SchemaItem
from sqlalchemy.types import TypeEngine

from alembic.operations.toimpl import Operations

from sqlalchemy import (create_engine, MetaData, Column,
                        Integer, String, Table)
import pprint

engine = create_engine("sqlite://")

engine.execute("""
create table foo (
    id integer not null primary key,
    old_data varchar,
    x integer
)"""
)

engine.execute('''
            create table bar (
                data varchar
            )''')

metadata = MetaData()
Table('foo', metadata,
      Column('id', Integer, primary_key=True),
      Column('data', Integer),
      Column('x', Integer, nullable=False)
      )
Table('bat', metadata,
      Column('info', String)
      )

ctx = MigrationContext.configure(engine.connect())

mc = produce_migrations(ctx, metadata)

ops = Operations(ctx)

op = mc.upgrade_ops.ops[0]

if __name__ == '__main__':

      print(op)
      print(ops.invoke(op))

# diff = compare_metadata(mc, metadata)
# pprint.pprint(diff, indent=2, width=20)
