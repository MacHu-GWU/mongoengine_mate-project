# -*- coding: utf-8 -*-

"""
This module extend the power of ``mongoengine.Document``.
"""

import math
import mongoengine
from copy import deepcopy
from collections import OrderedDict

from . import util

try:
    from typing import Type, Any, List, Dict
except ImportError:  # pragma: no cover
    pass

try:
    from pymongo.collection import Collection
    from pymongo.database import Database
    from mongoengine import QuerySet
except ImportError:  # pragma: no cover
    pass


class ExtendedDocument(mongoengine.Document):
    """
    Provide `mongoengine.Document <http://docs.mongoengine.org/apireference.html#mongoengine.Document>`_
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

        :rtype: str
        """
        return cls.id.name

    @classmethod
    def fields_ordered(cls):
        """
        Return declared field name in order.

        :rtype: List[str]
        """
        return list(cls._fields_ordered)

    def keys(self):
        """
        Convert to field list.

        :rtype: List[str]
        """
        return list(self._fields_ordered)

    def values(self):
        """
        Convert to field value list.

        :rtype: list
        """
        return [self._data.get(attr) for attr in self._fields_ordered]

    def items(self):
        """
        Convert to field and value pair list.

        :rtype: List[Tuple[str, Any]]
        """
        return [(attr, self._data.get(attr)) for attr in self._fields_ordered]

    def to_tuple(self):
        """
        Convert to field tuple.

        :rtype: Tuple[str]
        """
        return self._fields_ordered

    def to_list(self):
        """
        Convert to field list.

        :rtype: List[str]
        """
        return self.keys()

    def to_dict(self, include_none=True):
        """
        Convert to dict.

        :type include_none: bool
        :param include_none: if False, None value field will be removed.

        :rtype: Dict[str, Any]
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

        :type other: ExtendedDocument
        :rtype: None

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

        :type data: dict

        :rtype: None

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

        :rtype: Collection

        **中文文档**

        获得pymongo.Collection的实例。
        """
        return cls._get_collection()

    @classmethod
    def col(cls):
        """
        Alias of :meth:`~ExtendedDocument.collection()`

        :rtype: Collection
        """
        return cls._get_collection()

    @classmethod
    def database(cls):
        """
        Get connected pymongo Database instance.

        :rtype: Database
        """
        return cls._get_db()

    @classmethod
    def db(cls):
        """
        Alias of :meth:`~ExtendedDocument.database()`

        :rtype: Database
        """
        return cls._get_db()

    @classmethod
    def smart_insert(cls, data, minimal_size=5, n_insert=0, n_skipped=0):
        """
        An optimized Insert strategy.

        :type data: Union[ExtendedDocument, List[ExtendedDocument]]
        :type minimal_size: int

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
                n_insert += len(data)
            # 失败了
            except mongoengine.NotUniqueError:
                # 分析数据量
                n = len(data)
                # 如果数据条数多于一定数量
                if n >= minimal_size ** 2:
                    # 则进行分包
                    n_chunk = math.floor(math.sqrt(n))
                    for chunk in util.grouper_list(data, n_chunk):
                        n_insert, n_skipped = cls.smart_insert(chunk, minimal_size, n_insert, n_skipped)
                # 否则则一条条地逐条插入
                else:
                    for document in data:
                        try:
                            cls.objects.insert(document)
                            n_insert +=1
                        except mongoengine.NotUniqueError:
                            n_skipped +=1
        else:
            try:
                cls.objects.insert(data)
                n_insert += 1
            except mongoengine.NotUniqueError:
                n_skipped += 1
        return n_insert, n_skipped

    @classmethod
    def _smart_update(cls, obj, upsert=False):
        """
        Update one document, locate the document by _id, then only update
        the field defined with the ExtendedDocument instance. None field is
        ignored.

        :type obj: ExtendedDocument

        :rtype: int
        :return: 0 or 1, number of document been updated
        """
        if isinstance(obj, cls):
            dct = obj.to_dict(include_none=False)
            id_field_name = cls.id_field_name()
            if id_field_name in dct:
                dct.pop(id_field_name)
            return cls.objects(__raw__={"_id": obj.id}) \
                .update_one(upsert=upsert, **dct)
        else:  # pragma: no cover
            raise TypeError

    @classmethod
    def smart_update(cls, data, upsert=False, _insert_after_update=False):
        """
        Batch update with a lots orm data model.

        .. note::

            The batch update operation is not atomic. It can be done
            with transaction in MongoDB 4.0 +

        :type data: Union[ExtendedDocument, List[ExtendedDocument]]
        :param _insert_after_update: for developer use only, if True, will
            collect all to-insert document and bulk insert it at once after
            update.

        :rtype: Tuple[int, int]
        """
        n_update, n_insert = 0, 0
        if isinstance(data, list):
            if _insert_after_update:
                upsert = False
                to_insert_list = list()
                for obj in data:
                    update_flag = cls._smart_update(obj, upsert=upsert)
                    if not update_flag:
                        to_insert_list.append(obj)
                cls.smart_insert(to_insert_list)
                n_insert = len(to_insert_list)
                n_update = len(data) - n_insert
            else:
                for obj in data:
                    update_flag = cls._smart_update(obj, upsert=upsert)
                    if update_flag:
                        n_update += 1
                    else:
                        n_insert += 1
        else:
            update_flag = cls._smart_update(data, upsert=upsert)
            if update_flag:
                n_update += 1
            else:
                n_insert += 1

        return n_update, n_insert

    @classmethod
    def by_id(cls, _id):
        """
        Get one document instance by _id.

        :rtype: ExtendedDocument

        **中文文档**

        根据_id, 返回一条文档。
        """
        return cls.objects(__raw__={"_id": _id}).get()

    @classmethod
    def by_filter(cls, filters):
        """
        Filter objects by pymongo dict query.

        :rtype: QuerySet

        **中文文档**

        使用pymongo的API进行查询。
        """
        return cls.objects(__raw__=filters)

    @classmethod
    def random_sample(cls, filters=None, n=5):
        """
        Randomly select n samples.

        :type filters: Union[Dict, None]
        :param filters: nature pymongo query dictionary.

        :type n: int
        :param n: number of document you want to select.

        :rtype: List[ExtendedDocument]

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
