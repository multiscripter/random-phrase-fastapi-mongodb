from datetime import datetime
from fastapi import HTTPException
from models.phrase import Phrase
from pymongo import MongoClient
from typing import List


class PhraseRepository:
    """Phrase repository."""

    def __init__(self, db_name: str, cln_name: str) -> None:
        """Constructor."""

        client = MongoClient()
        db = client[db_name]
        self.collection = db[cln_name]

    def get(self, criteria: dict = None) -> List[Phrase]:
        """Gets a list of all phrases."""

        result = []
        for found in self.collection.find(criteria):
            phrase = Phrase(**found)
            result.append(phrase)
        return result

    def create(self, data: dict) -> Phrase:
        """Creates a phrase."""

        data['id'] = self.collection.count_documents({}) + 1
        data['date'] = datetime.utcnow()
        result = self.collection.insert_one(data)
        if result.acknowledged:
            return Phrase(**data)
        else:
            HTTPException(400, 'Creation error')

    def delete(self, data: dict) -> int:
        """Deletes a phrase."""

        criteria = {
            'id': {'$eq': data['id']}
        }
        result = self.collection.delete_many(criteria)
        if result.acknowledged:
            return result.deleted_count
        else:
            HTTPException(400, 'Deletion error')

    def update(self, id: int, data: dict) -> int:
        """Updates a phrase."""

        criteria = {'id': id}
        data = {'$set': data}
        result = self.collection.update_one(criteria, data)
        if result.acknowledged:
            return result.modified_count
        else:
            HTTPException(400, 'Update error')
