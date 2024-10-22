#!/usr/bin/env python3
"""
List all documents in a collection
"""

from pymongo import MongoClient


def list_all(mongo_collection):
    """Return list all documents"""
    documents = mongo_collection.find()
    return documents