#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module extend the power of mongoengine.Document.
"""

import math
import mongoengine
from copy import deepcopy
from collections import OrderedDict

try:
    from . import util
except ImportError:  # pragma: no cover
    from mongoengine_mate import util


class ExtendedDocument(mongoengine.Document):
    """Provide `mongoengine.Document <http://docs.mongoengine.org/apireference.html#mongoengine.Document>`_
    more utility methods.

    **中文文档**

    为默认的 ``mongoengine.Document`` 提供了更多的便捷方法。
    """
    meta = {
        "abstract": True,
    }

    @classmethod
    def id_field_name(cls):
        """
        Return the ``_id`` field name.

        :return: str
        """
        return cls.id.name

    @classmethod
    def fields_ordered(cls):
        """
        Return declared field name in order.
        """
        return list(cls._fields_ordered)

    def keys(self):
        """
        Convert to field list.
        """
        return list(self._fields_ordered)

    def values(self):
        """
        Convert to field value list.
        """
        return [self._data.get(attr) for attr in self._fields_ordered]

    def items(self):
        """
        Convert to field and value pair list.
        """
        return [(attr, self._data.get(attr)) for attr in self._fields_ordered]

    def to_tuple(self):
        """
        Convert to field tuple.
        """
        return self._fields_ordered

    def to_list(self):
        """
        Convert to field list.
        """
        return self.keys()

    def to_dict(self, include_none=True):
        """
        Convert to dict.

        :param include_none: bool, if False, None value field will be removed.
        """
        if include_none:
            return dict(self.items())
        else:
            return {
                key: value
                for key, value in self.items()
                if value is not None
            }

    def to_OrderedDict(self, include_none=True):
        """
        Convert to OrderedDict.

        :param include_none: bool, if False, None value field will be removed.
        """
        if include_none:
            return OrderedDict(self.items())
        else:
            return OrderedDict([
                (key, value)
                for key, value in self.items()
                if value is not None
            ])

    def __repr__(self):
        kwargs = list()
        for attr, value in self.items():
            kwargs.append("%s=%r" % (attr, value))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(kwargs))

    def __str__(self):
        return self.__repr__()

    def absorb(self, other):
        """
        For attributes of others that value is not None, assign it to self.

        **中文文档**

        将另一个文档中的数据更新到本条文档。当且仅当数据值不为None时。
        """
        if not isinstance(other, self.__class__):
            raise TypeError

        for attr, value in other.items():
            if value is not None:
                setattr(self, attr, deepcopy(value))

    def revise(self, data):
        """
        Revise attributes value with dictionary data.

        **中文文档**

        将一个字典中的数据更新到本条文档。当且仅当数据值不为None时。
        """
        if not isinstance(data, dict):
            raise TypeError

        for key, value in data.items():
            if value is not None:
                setattr(self, key, deepcopy(value))

    @classmethod
    def collection(cls):
        """
        Get pymongo Collection instance.

        **中文文档**

        获得pymongo.Collection的实例。
        """
        return cls._get_collection()

    @classmethod
    def col(cls):
        """
        Alias of :meth:`~ExtendedDocument.collection()`
        """
        return cls._get_collection()

    @classmethod
    def database(cls):
        """
        Get connected pymongo Database instance.
        """
        return cls._get_db()

    @classmethod
    def db(cls):
        """
        Alias of :meth:`~ExtendedDocument.database()`
        """
        return cls._get_db()

    @classmethod
    def smart_insert(cls, data, minimal_size=5):
        """
        An optimized Insert strategy.

        **中文文档**

        在Insert中, 如果已经预知不会出现IntegrityError, 那么使用Bulk Insert的速度要
        远远快于逐条Insert。而如果无法预知, 那么我们采用如下策略:

        1. 尝试Bulk Insert, Bulk Insert由于在结束前不Commit, 所以速度很快。
        2. 如果失败了, 那么对数据的条数开平方根, 进行分包, 然后对每个包重复该逻辑。
        3. 若还是尝试失败, 则继续分包, 当分包的大小小于一定数量时, 则使用逐条插入。
          直到成功为止。

        该Insert策略在内存上需要额外的 sqrt(nbytes) 的开销, 跟原数据相比体积很小。
        但时间上是各种情况下平均最优的。
        """
        if isinstance(data, list):
            # 首先进行尝试bulk insert
            try:
                cls.objects.insert(data)
            # 失败了
            except mongoengine.NotUniqueError:
                # 分析数据量
                n = len(data)
                # 如果数据条数多于一定数量
                if n >= minimal_size ** 2:
                    # 则进行分包
                    n_chunk = math.floor(math.sqrt(n))
                    for chunk in util.grouper_list(data, n_chunk):
                        cls.smart_insert(chunk, minimal_size)
                # 否则则一条条地逐条插入
                else:
                    for document in data:
                        try:
                            cls.objects.insert(document)
                        except mongoengine.NotUniqueError:
                            pass
        else:
            try:
                cls.objects.insert(data)
            except mongoengine.NotUniqueError:
                pass

    @classmethod
    def _smart_update(cls, obj):
        if isinstance(obj, cls):
            dct = obj.to_dict(include_none=False)
            id_field_name = cls.id_field_name()
            if id_field_name in dct:
                dct.pop(id_field_name)
            return cls.objects(__raw__={"_id": obj.id}) \
                .update_one(upsert=True, **dct)
        else:  # pragma: no cover
            raise TypeError

    @classmethod
    def smart_update(cls, data):
        """

        :param data:
        :param filters:
        :return:
        """
        if isinstance(data, list):
            for obj in data:
                cls._smart_update(obj)
        else:
            cls._smart_update(data)

    @classmethod
    def by_id(cls, _id):
        """
        Get one instance by _id.

        **中文文档**

        根据_id, 返回一条文档。
        """
        return cls.objects(__raw__={"_id": _id}).get()

    @classmethod
    def by_filter(cls, filters):
        """
        Filter objects by pymongo dict query.

        **中文文档**

        使用pymongo的API进行查询。
        """
        return cls.objects(__raw__=filters)

    @classmethod
    def random_sample(cls, filters=None, n=5):
        """
        Randomly select n samples.

        :param filters: nature pymongo query dictionary.
        :param n: number of document you want to select.

        **中文文档**

        随机选择 ``n`` 个样本。
        """
        data = list()

        id_field = cls._meta["id_field"]

        pipeline = list()
        if filters is not None:
            filters = dict(filters)
            if id_field != "_id":
                filters["_id"] = filters[id_field]
                del filters[id_field]
            pipeline.append({"$match": filters})
        pipeline.append({"$sample": {"size": n}})

        col = cls.col()

        if id_field == "_id":
            for doc in col.aggregate(pipeline):
                obj = cls(**doc)
                data.append(obj)

        else:
            for doc in col.aggregate(pipeline):
                doc[id_field] = doc["_id"]
                del doc["_id"]
                obj = cls(**doc)
                data.append(obj)

        return data
