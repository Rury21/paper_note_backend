from typing import List, Optional

from pydantic import BaseModel


class PaperPost(BaseModel):
    title: str
    year: int
    tags: Optional[List[str]]
    url: Optional[str]
    abstract: Optional[str]
    references: Optional[List[str]]


class Paper(PaperPost):
    id: str
