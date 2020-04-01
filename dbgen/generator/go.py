from sqlalchemy import Column, Table, Boolean, Float
from pydantic import BaseModel
from typing import List

from dbgen.utils.functions import to_camel_case

TYPE_MAP = {
    'Integer': 'int64',
    'String': 'string',
    'Boolean': 'bool',
    'Float': 'float64'
}


class StructField(BaseModel):
    name: str
    type: str
    tag: str


class Struct(BaseModel):
    name: str
    fields: List[StructField]


def generate_column(column: Column) -> StructField:
    return StructField(
        name=to_camel_case(column.name),
        type=TYPE_MAP[str(column.type)],
        tag=f'`db:"{column.name}"`'
    )


def generate_table(table: Table) -> Struct:
    return Struct(
        name=to_camel_case(table.name),
        fields=[generate_column(column) for column in table.columns]
    )
