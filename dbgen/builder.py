from typing import List, Dict

import sqlalchemy
import yaml
from pydantic import BaseModel


class ConstraintBuilder(BaseModel):
    type: str
    columns: List[str]
    name: str = ''

    # class Config:
    #     arbitrary_types_allowed = True

    def build(self) -> sqlalchemy.Constraint:
        pass


TYPE_MAP = {
    'string': sqlalchemy.String,
    'int': sqlalchemy.Integer
}


class ForeignBuilder(BaseModel):
    to: str
    on_update: str = ''
    on_delete: str = ''

    # class Config:
    #     arbitrary_types_allowed = True


class ColumnBuilder(BaseModel):
    name: str
    type: str
    primary_key: bool = False
    nullable: bool = False
    index: bool = False
    unique: bool = False
    foreign: ForeignBuilder = None

    # class Config:
    #     arbitrary_types_allowed = True

    def build(self) -> sqlalchemy.Column:
        return sqlalchemy.Column(
            self.name, TYPE_MAP[self.type],
            primary_key=self.primary_key,
            nullable=self.nullable,
            index=self.index,
            unique=self.unique
        )


class TableBuilder(BaseModel):
    name: str
    columns: List[ColumnBuilder]
    constraints: List[ConstraintBuilder] = None

    # class Config:
    #     arbitrary_types_allowed = True

    def build(self, metadata: sqlalchemy.MetaData) -> sqlalchemy.Table:
        args = [column.build() for column in self.columns]
        if self.constraints:
            args.extend([constraint.build() for constraint in self.constraints])

        return sqlalchemy.Table(self.name, metadata, *args)


class Database(BaseModel):
    metadata: sqlalchemy.MetaData
    tables: Dict[str, sqlalchemy.Table]

    class Config:
        arbitrary_types_allowed = True


class DatabaseBuilder(BaseModel):
    url: str
    tables: List[TableBuilder]

    @classmethod
    def load_from_file(cls, file: str) -> 'DatabaseBuilder':
        with open(file, 'r') as f:
            kwargs = yaml.load(f.read(), yaml.SafeLoader)

        return cls(**kwargs)

    def build(self) -> Database:
        metadata = sqlalchemy.MetaData()
        tables = {table.name: table.build(metadata) for table in self.tables}

        return Database(metadata=metadata, tables=tables)
