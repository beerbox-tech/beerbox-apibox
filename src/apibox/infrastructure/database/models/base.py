"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

apibox base class for all database models
see https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html
section "Creating an Explicit Base Non-Dynamically"
"""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import registry
from sqlalchemy.orm.decl_api import DeclarativeMeta

mapper_registry = registry()


class DatabaseModel(metaclass=DeclarativeMeta):
    """base class for all database models"""

    __abstract__ = True

    registry = mapper_registry
    metadata = mapper_registry.metadata
    type_annotation_map = {datetime: DateTime(timezone=True)}

    __init__ = mapper_registry.constructor
