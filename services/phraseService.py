from datetime import datetime

import pymongo
from fastapi import HTTPException
from starlette.datastructures import QueryParams
from models.phrase import Phrase
from pymongo import MongoClient
from typing import List


class PhraseService:
    """Phrase service."""

    def __init__(self, db_name: str, cln_name: str) -> None:
        """Constructor."""

        client = MongoClient()
        db = client[db_name]
        self.collection = db[cln_name]
        self.last_id = self.collection.find({}).sort(
            'id', pymongo.DESCENDING
        ).limit(1).next()['id']

    def get(self, params: QueryParams = None) -> List[Phrase]:
        """Gets a list of all phrases."""

        # https://developerslogblog.wordpress.com/2019/10/15/mongodb-how-to-filter-by-multiple-fields/

        result = []
        criteria = {}
        if params:
            if 'random' in params:
                val = params['random']
                val = int(val) if val.isdigit() else 1
                if val < 1:
                    val = 1
                cursor = self.collection.aggregate([
                    {'$sample': {'size': val}}
                ])
            else:
                fields = Phrase.__fields__.keys()
                for key in params:
                    if key in fields:
                        val = params[key]
                        if val.isdigit():
                            val = int(val)
                        criteria[key] = val
                cursor = self.collection.find(criteria)
        else:
            cursor = self.collection.find()
        for found in cursor:
            phrase = Phrase(**found)
            result.append(phrase)
        return result

    def create(self, data: dict) -> Phrase:
        """Creates a phrase."""

        data['id'] = self.last_id + 1
        data['date'] = datetime.utcnow()
        result = self.collection.insert_one(data)
        if result.acknowledged:
            self.last_id += 1
            return Phrase(**data)
        else:
            raise HTTPException(400, 'Creation error')

    def delete(self, id: int) -> int:
        """Deletes a phrase."""

        criteria = {
            'id': {'$eq': id}
        }
        result = self.collection.delete_many(criteria)
        if result.acknowledged:
            return result.deleted_count
        else:
            raise HTTPException(400, 'Deletion error')

    def update(self, id: int, data: dict) -> int:
        """Updates a phrase."""

        criteria = {'id': id}
        data = {'$set': data}
        result = self.collection.update_one(criteria, data)
        if result.acknowledged:
            return result.modified_count
        else:
            raise HTTPException(400, 'Update error')
