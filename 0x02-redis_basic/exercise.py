#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, 
store an instance of the Redis client as a private variable named _redis (using redis.Redis())
and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string. 
The method should generate a random key (e.g. using uuid), 
store the input data in Redis using the random key and return the key.
"""

from curses import keyname
from unittest import result
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """The count calls function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """The call history method"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        input = key + ':inputs'
        output = key + ':outputs'
        data = str(args)
        self._redis.rpush(input, data)
        final = method(self, *args, **kwargs)
        self._redis.rpush(output, str(final))
        return final
    return wrapper


def replay(func: Callable):
    """the replay method"""
    r = redis.Redis()
    key = func.__qualname__
    input = r.lrange(f"{key}:inputs", 0, -1)
    output = r.lrange(f"{key}:outputs", 0, -1)
    count_calls = len(input)
    times_str = 'times'
    if count_calls == 1:
        times_str = 'time'
    final = f"{key} was called {count_calls} {times_str}"
    print(final)
    for k, v in zip(input, output):
        final = "{}(*{},) -> {}".format(
            key,
            k.decode('utf-8'),
            v.decode('utf-8')
        )
        print(final)


class Cache:
    """Class to store data attached to random keys in Redis"""
    def __init__(self):
        """The init method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in redis, returns unique
        random key as a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes,
                                                          int, float, None]:
        """Converts data back to desired format"""
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """get string format of value pointed to by key"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """get int representation of value paired to key"""
        return self.get(key, fn=int)