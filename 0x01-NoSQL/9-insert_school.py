#!/usr/bin/env python3

"""
Insert a new document in a collection based
on kwargs
"""

from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """Return new document inserted"""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id