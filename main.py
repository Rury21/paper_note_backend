import string
from typing import List

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

import database as db
from shemas import Paper, PaperPost

app = FastAPI()
origins = ["https://paper-note-frontend.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "paper api"}


@app.get("/api/papers/", response_model=List[Paper])
async def get_all_papers():
    papers = await db.get_all_papers()
    return papers


@app.get("/api/search/tag/{tag}/", response_model=List[Paper])
async def get_papers_by_tag(tag: str):
    papers = await db.get_papers_by_tag(tag)
    return papers


@app.get("/api/search/title/{title}/", response_model=List[Paper])
async def get_papers_by_title(title: str):
    papers = await db.get_papers_by_title(title)
    return papers


@app.post("/api/papers/", response_model=Paper)
async def create_paper(data: PaperPost):
    paper = await db.create_paper(data.dict())
    if paper:
        return paper
    raise HTTPException(status.HTTP_400_BAD_REQUEST, "Create failed")


@app.get("/api/paper/{id}/", response_model=Paper)
async def get_one_paper(id: str):
    paper = await db.get_one_paper(id)
    if paper:
        return paper
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"There is no paper id:{id}")


@app.put("/api/paper/{id}/", response_model=Paper)
async def update_paper(id: str, data: PaperPost):
    paper = await db.update_paper(id, data.dict())
    if paper:
        return paper


@app.delete("/api/paper/{id}/")
async def delete_todo(id: str):
    is_success = await db.delete_paper(id)
    if is_success:
        return {"Successfully deleted paper"}
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"delete failed id:{id}")
