from datetime import datetime

import pymongo
from fastapi import HTTPException
from starlette.datastructures import QueryParams
from models.category import Category
from models.phrase import Phrase
from pymongo import MongoClient
from typing import List


class PhraseService:
    """Phrase service."""

    def __init__(self, db_name: str, cln_name: List[str]) -> None:
        """Constructor."""

        client = MongoClient()
        db = client[db_name]
        self.phrases = db[cln_name[0]]
        self.cats = db[cln_name[1]]
        self.last_id = self.phrases.find({}).sort(
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
                pipeline = []
                # Выбрать случайную цитату из категории.
                if 'category.id' in params:
                    id = params['category.id']
                    if id.isdigit():
                        id = int(id)
                        if id > 0:
                            pipeline.append({'$match': {'category.id': id}})
                pipeline.append({'$sample': {'size': val}})
                cursor = self.phrases.aggregate(pipeline)
            else:
                p_fields = Phrase.__fields__.keys()
                params = params.__str__().split('&')
                params = [p.split('=') for p in params]
                for param in params:
                    if param[0].startswith('category.'):
                        c_fields = Category.__fields__.keys()
                        kv = param[0].split('.')
                        if kv[1] in c_fields:
                            val = param[1]
                            if val.isdigit():
                                val = int(val)
                            if kv[1] == 'id' and val < 1:
                                continue
                            criteria[f'{param[0]}'] = val
                    else:
                        if param[0] in p_fields:
                            val = param[1]
                            if val.isdigit():
                                val = int(val)
                            criteria[f'{param[0]}'] = val
                cursor = self.phrases.find(criteria)
        else:
            cursor = self.phrases.find()
        for found in cursor:
            phrase = Phrase(**found)
            result.append(phrase)
        return result

    def create(self, data: dict) -> Phrase:
        """Creates a phrase."""

        data['id'] = self.last_id + 1
        data['date'] = datetime.utcnow()
        result = self.phrases.insert_one(data)
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
        result = self.phrases.delete_many(criteria)
        if result.acknowledged:
            return result.deleted_count
        else:
            raise HTTPException(400, 'Deletion error')

    def update(self, id: int, data: dict) -> int:
        """Updates a phrase."""

        criteria = {'id': id}
        data = {'$set': data}
        result = self.phrases.update_one(criteria, data)
        if result.acknowledged:
            return result.modified_count
        else:
            raise HTTPException(400, 'Update error')

    def get_index_data(self) -> dict:
        """Gets data for index page."""

        data = dict()
        data['categories'] = []
        data['count'] = dict()
        data['count'][0] = 0
        cursor = self.cats.find()
        for found in cursor:
            cat = Category(**found)
            data['categories'].append(cat)
            criteria = {'category.id': cat.id}
            data['count'][cat.id] = self.phrases.count_documents(criteria)
            data['count'][0] += data['count'][cat.id]
        return data
