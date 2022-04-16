import json
from typing import Optional

import aioredis
from core.settings import app_configs


class RedisManager:
    def __init__(self):
        self.redis_connection: Optional[aioredis.Redis] = None

    def init_redis(self):
        self.redis_connection = aioredis.from_url(
            f'redis://{app_configs.REDIS_HOST}:{app_configs.REDIS_PORT}',
            db=app_configs.REDIS_DBNAME,
            encoding="utf-8",
            decode_responses=True,
        )

    def make_cache_key(self, key, key_prefix=app_configs.REDIS_KEY_PREFIX, version=None):
        """Method to format cache key

        Args:
            key ([str]):cache_key
            key_prefix ([str], optional): [key_prefix]. Defaults to app_configs.REDIS_KEY_PREFIX.
            version ([str], optional): [cache version]. Defaults to None.

        Returns:
            [str]: [formatted key]
        """

        return f'{key_prefix}:{key}'

    async def set_hash_field(self, key, field, value, ttl=None):
        """[Method to set the string value of a hash field.
            If key does not exist, a new key holding a hash is created.
            If field already exists in the hash, it is overwritten].

        Args:
            key ([str]): [cache key]
            field ([str]): [field of the cache key]
            value ([str]): [ value of the field]
            ttl ([int], optional): [expire time of cache key]. Defaults to None.
        """

        await self.redis_connection.hset(self.make_cache_key(key), field, value)
        if ttl:
            await self.redis_connection.expire(self.make_cache_key(key), ttl)

    async def get_hash_field(self, key, field):
        """[Method to get the value associated with field in the hash stored at key]

        Args:
            key ([str]): [cache key]
            field ([str]): [field of the cache key whose value needs to be found]

        Returns:
            [str]: [the value associated with field or None]
        """

        key_value = await self.redis_connection.hget(self.make_cache_key(key), field)

        return key_value if key_value else None

    async def set_dict_hash_field(self, key, field, value, ttl=None):
        """[Method to set a dictionary/object value of a hash field.
            If key does not exist, a new key holding a hash is created.
            If field already exists in the hash, it is overwritten].

        Args:
            key ([str]): [cache key]
            field ([str]): [field of the cache key]
            value ([object]): [ object] eg: {"name":"saniya"}
            ttl ([int], optional): [expire time of cache key]. Defaults to None.
        """

        await self.redis_connection.hset(self.make_cache_key(key), field, json.dumps(value))
        if ttl:
            await self.redis_connection.expire(self.make_cache_key(key), ttl)

    async def get_dict_hash_field(self, key, field):
        """[Method to get the value associated with field in the hash stored at key]

        Args:
            key ([str]): [cache key]
            field ([str]): [field of the cache key whose value needs to be found]

        Returns:
            [dict]: [the value associated with field or {}]
        """

        key_value = await self.redis_connection.hget(self.make_cache_key(key), field)

        if key_value:
            value = json.loads(key_value)
            return value
        else:
            return {}

    async def set_multiple_hash_fields(self, key, field_map, ttl=None):
        """[Method to set multiple hash fields to multiple values]

        Args:
            key ([str]): [cache key]
            field_map ([obj]): [field and value map of the cache key]
            ttl ([int], optional): [cache key expiry time]. Defaults to None.

        """

        await self.redis_connection.hmset(self.make_cache_key(key), field_map)
        if ttl:
            await self.redis_connection.expire(self.make_cache_key(key), ttl)

    async def get_multiple_hash_fields(self, key, fields):
        """[Method to fetch the values of all the given fields]

        Args:
            key ([str]): [description]
            fields ([list]): [List of fields whose value to be find]

        Returns:
            [list]: [list of values]
        """

        value_list = []
        if fields:

            values = await self.redis_connection.hmget(self.make_cache_key(key), *fields)
            value_list = [value for value in values if value]
        return value_list

    async def get_all_hash_fields(self, key):
        """[Method to fetch the all the field, value of the given key]

        Args:
            key ([str]): [description]

        Returns:
            [list]: [list of values]
        """

        value_list = []
        values = await self.redis_connection.hgetall(self.make_cache_key(key))
        value_list = [value for value in values if value]
        return value_list

    async def delete_hash_field(self, key, field):
        """[Method to delete any field of cache key]

        Args:
            key ([str]): [cache key]
            field ([str]): [the field which needs to be deleted]
        """

        await self.redis_connection.hdel(self.make_cache_key(key), field)

    async def set_value(self, key, value, ttl=None):
        """[Method to set key to hold the string value. If key already holds a value, it is overwritten]

        Args:
            key ([str]): [key to be set]
            value ([str]): [value of the key]
            ttl ([int], optional): [expire time of cache key]. Defaults to None.
        """

        if ttl:
            await self.redis_connection.set(self.make_cache_key(key), value, ex=ttl)
        else:
            await self.redis_connection.set(self.make_cache_key(key), value)

    async def get_value(self, key):
        """[Method to get value for a key]

        Args:
            key ([str]): [cache key]

        Returns:
            [str]: [key value]
        """

        key_value = await self.redis_connection.get(self.make_cache_key(key))
        return key_value if key_value else None

    async def set_field_if_not_exists(self, key, value, ttl=None):
        """[Method to set key to string value if key does not exist and
            when key already holds a value, no operation is performed]

        Args:
            key ([str]): [key to be set]
            value ([str]): [value of the key]
            ttl ([int], optional): [expire time of cache key]. Defaults to None.

        Returns:
            [Boolean]: [True If value is set else False]
        """

        is_set = await self.redis_connection.setnx(self.make_cache_key(key), value)
        if ttl:
            await self.redis_connection.expire(self.make_cache_key(key), ttl)
        if is_set:
            return True
        else:
            return False

    async def add_to_set(self, key, value, ttl=None):
        """[Method to add value to set for a cache key]

        Args:
            key ([str]): [ key to be set]
            value ([list]): [value to be added to set]
            ttl ([int], optional): [expire time of cache key]. Defaults to None.
        """

        await self.redis_connection.sadd(self.make_cache_key(key), value)
        if ttl:
            await self.redis_connection.expire(self.make_cache_key(key), ttl)

    async def get_values_in_set(self, key):
        """[Method to get members in a set for a cache key]

        Args:
            key ([str]): [cache key]

        Returns:
            [list]: [set of values]
        """

        values = await self.redis_connection.smembers(self.make_cache_key(key))
        return [value for value in values]

    async def remove_from_set(self, key, value):
        """[Method to remove a member from a set for a cache key]

        Args:
            key ([str]): [cache key]
            value ([str]): [value to be removed from set]
        """
        await self.redis_connection.srem(self.make_cache_key(key), value)

    async def is_value_in_set(self, key, value):
        """[Method to check is a value is in a set for a cache key]

        Args:
            key ([str]): [key to be searched]
            value ([str]): [value to check]

        Returns:
            [Boolean]: [True if value found else False]
        """

        return await self.redis_connection.sismember(self.make_cache_key(key), value)

    async def values_count_in_set(self, key):
        """[Method to count the values is in a set for a cache key]

        Args:
            key ([str]): [ key to be searched]

        Returns:
            [int]: [count of the number of values]
        """

        return await self.redis_connection.scard(self.make_cache_key(key))

    async def delete_key(self, key):
        """[Method to delete key from redis]

        Args:
            key ([str]): [key to be delete]

        Returns:
            [Boolena]: [ True if found and deleted else False]
        """

        if not isinstance(key, list):
            key_list = [self.make_cache_key(key)]
        else:
            key_list = [self.make_cache_key(key_name) for key_name in key]

        return await self.redis_connection.delete(*key_list)


redis_cache = RedisManager()
