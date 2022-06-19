import motor.motor_asyncio
from bson import ObjectId
from decouple import config

MONGO_API_KEY = config("MONGO_API_KEY")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
database = client.Paper_DB
collection_paper = database.paper


def paper_serializer(paper):
    return {
        "id": str(paper["_id"]),
        "title": paper["title"],
        "year": paper["year"],
        "tags": paper["tags"],
        "references": paper["references"],
        "url": paper["url"],
        "abstract": paper["abstract"],
    }


async def create_paper(data: dict):
    result = await collection_paper.insert_one(data)
    new_paper = await collection_paper.find_one({"_id": result.inserted_id})
    if new_paper:
        return paper_serializer(new_paper)
    return False


async def get_all_papers():
    papers = []
    cursor = collection_paper.find()
    for paper in await cursor.to_list(length=100):
        papers.append(paper_serializer(paper))
    return papers


async def get_one_paper(id: str):
    paper = await collection_paper.find_one({"_id": ObjectId(id)})
    if paper:
        return paper_serializer(paper)
    return False


async def get_papers_by_tag(tag: str):
    papers = []
    cursor = collection_paper.find({"tags": {"$in": [tag]}})
    for paper in await cursor.to_list(length=100):
        papers.append(paper_serializer(paper))
    return papers


async def get_papers_by_title(title: str):
    papers = []
    cursor = collection_paper.find(filter={"title": {"$regex": title}})
    for paper in await cursor.to_list(length=100):
        papers.append(paper_serializer(paper))
    return papers


async def update_paper(id: str, data: dict):
    paper = await collection_paper.find_one({"_id": ObjectId(id)})
    if paper:
        result = await collection_paper.update_one(
            {"_id": ObjectId(id)},
            {"$set": data},
        )
        new_paper = await collection_paper.find_one({"_id": ObjectId(id)})
        return paper_serializer(new_paper)
    return False


async def delete_paper(id: str):
    paper = await collection_paper.find_one({"_id": ObjectId(id)})
    if paper:
        result = await collection_paper.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return True
    return False
