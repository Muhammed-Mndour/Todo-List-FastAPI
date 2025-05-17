from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from typing import Dict, Type, Optional, Any
from jsql import sql
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def insert_row(conn: Any, table: Type[Base], row: Dict[str, Any], ignore: bool = False) -> Optional[int]:
    """
    Insert a single row into a database table.

    Args:
        conn: Database connection object
        table: SQLAlchemy model class
        row: Dictionary containing column names and values to insert
        ignore: If True, uses INSERT IGNORE to skip duplicate entries

    Returns:
        The ID of the inserted row if available, otherwise None

    Raises:
        SQLAlchemyError: If the database operation fails
    """
    # Get valid columns (intersection of table columns and provided data)
    valid_columns = set(table.__table__.columns.keys()) & set(row.keys())

    if not valid_columns:
        raise ValueError(f"No valid columns found for table {table.__tablename__}")

    # Filter the row data to only include valid columns
    filtered_row = {k: row[k] for k in valid_columns}

    return sql(
        conn,
        '''
        INSERT {% if ignore %}IGNORE{% endif %} 
        INTO {% if schema %}`{{schema}}`.{% endif %}`{{ table }}` 
            ({% for column in columns %}`{{ column }}`{{ comma if not loop.last }}{% endfor %})
        VALUES 
            ({% for column in columns %}:{{ column }}{{ comma if not loop.last }}{% endfor %})
        ''',
        schema=table.__table__.schema,
        table=table.__tablename__,
        columns=valid_columns,
        ignore=ignore,
        **filtered_row,
    )
