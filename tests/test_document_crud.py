# -*- coding: utf-8 -*-

import pytest

import sys
from pymongo.database import Database
import mongoengine
from mongoengine_mate import ExtendedDocument

py_ver = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
user_col_name = "user_%s" % py_ver
item_col_name = "item_%s" % py_ver


class User(ExtendedDocument):
    user_id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()

    meta = {
        "collection": user_col_name
    }


class Item(ExtendedDocument):
    _id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()

    meta = {
        "collection": item_col_name
    }


# --- CRUD ---
def test_collection(connect):
    assert User.collection().name == user_col_name
    assert User.col().name == user_col_name


def test_database(connect):
    assert isinstance(User.database(), Database)
    assert isinstance(User.db(), Database)


def test_query(connect):
    User(user_id=1, name="Jack").save()
    User(user_id=2, name="Tom").save()

    assert User.by_id(1).name == "Jack"
    assert User.by_filter({"_id": 2})[:][0].name == "Tom"


def test_smart_insert(connect):
    import time
    import random

    n_exist = 5
    n_total = 200

    # Smart Insert
    User.objects.delete()

    user_id_list = [random.randint(1, n_total) for _ in range(n_exist)]
    user_id_list = list(set(user_id_list))
    user_id_list.sort()

    exist_users = [User(user_id=user_id) for user_id in user_id_list]
    User.objects.insert(exist_users)
    assert User.objects.count() == len(user_id_list)

    total_users = [User(user_id=i) for i in range(1, 1 + n_total)]

    st = time.clock()
    User.smart_insert(total_users)
    elapse1 = time.clock() - st

    assert User.objects.count() == n_total  # after smart insert, we got 400 doc

    # Regular Insert
    User.objects.delete()

    exist_users = [User(user_id=user_id) for user_id in user_id_list]
    User.objects.insert(exist_users)
    assert User.objects.count() == len(user_id_list)

    total_users = [User(user_id=i) for i in range(1, 1 + n_total)]

    st = time.clock()
    for user in total_users:
        try:
            user.save()
        except:
            pass
    elapse2 = time.clock() - st

    assert User.objects.count() == n_total  # after regular insert, we got 400 doc

    assert elapse1 <= elapse2

    # Single Document Insert
    User.smart_insert(User(id=1))


def test_random_sample(connect):
    User.smart_insert([User(user_id=i) for i in range(100)])
    assert len(User.random_sample(n=3)) == 3
    for user in User.random_sample(filters={"user_id": {"$gte": 50}}, n=3):
        assert user.user_id >= 50

    Item.smart_insert([Item(_id=i) for i in range(100)])
    assert len(Item.random_sample(n=3)) == 3
    for item in Item.random_sample(filters={"_id": {"$gte": 50}}, n=3):
        assert item._id >= 50


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
