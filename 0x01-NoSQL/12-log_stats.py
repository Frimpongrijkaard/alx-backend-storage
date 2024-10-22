#!/usr/bin/env python3
"""
This module provide stats about
Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def get_stats():
    """Get Nginx log stats"""
    client = MongoClient('mongodb://localhost:27017')
    nginx = client.logs.nginx
    print(f"{nginx.count_documents({})} logs")
    print("Methods:")
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        count = nginx.count_documents({'method': method})
        print(f"\tmethod {method}: {count}")
    get_count = nginx.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{get_count} status check")


if __name__ == "__main__":
    get_stats()