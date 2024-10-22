#!/usr/bin/env python3
"""
This module returns list of school offering
a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """Return a List schools offering given topic"""
    results = mongo_collection.find({"topics": topic})
    return results