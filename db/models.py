from typing import Optional
from sqlmodel import Field, SQLModel

class Search(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    query: str
    websites: str
    query_type: str
    results: str
    num_results: int
    timestamp: str

