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
