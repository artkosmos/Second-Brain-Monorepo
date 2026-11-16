from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at_datetime = Annotated[
    datetime,
    mapped_column(
        server_default=func.timezone("utc", func.now()),
    ),
]
updated_at_datetime = Annotated[
    datetime,
    mapped_column(
        server_default=func.timezone("utc", func.now()),
        onupdate=func.timezone("utc", func.now()),
    ),
]
