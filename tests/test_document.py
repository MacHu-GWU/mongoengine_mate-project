#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx

import sys
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


def test_keys_values_items(connect):
    user = User(user_id=1, name="Jack")

    assert user.keys() == ["user_id", "name"]
    assert user.values() == [1, "Jack"]
    assert user.items() == [("user_id", 1), ("name", "Jack")]


def test_repr(connect):
    user = User(user_id=1)
    assert str(user) == "User(user_id=1, name=None)"


def test_to_tuple_list_dict_OrderedDict_json(connect):
    user = User(user_id=1, name="Jack")

    assert user.to_tuple() == ("user_id", "name")
    assert user.to_list() == ["user_id", "name"]
    assert user.to_dict() == {"user_id": 1, "name": "Jack"}
    assert user.to_OrderedDict() == {"user_id": 1, "name": "Jack"}

    assert user.to_json() == '{"_id": 1, "name": "Jack"}'


def test_absorb_and_revise(connect):
    user = User(id=1, name="Jack")
    user.absorb(User(name="Tom"))
    assert user.name == "Tom"

    class MyClass(object): pass

    with raises(TypeError):
        user.absorb(MyClass())


def test_revise(connect):
    user = User(id=1, name="Jack")
    user_data = {"name": "Tom"}
    user.revise(user_data)
    assert user.name == "Tom"

    with raises(TypeError):
        user.revise([("name", "Tome")])


def test_collection(connect):
    assert User.collection().name == user_col_name
    assert User.col().name == user_col_name


def test_query(connect):
    User(user_id=1, name="Jack").save()
    User(user_id=2, name="Tom").save()

    assert User.by_id(1).name == "Jack"
    assert User.by_filter({"_id": 2})[:][0].name == "Tom"


def test_smart_insert(connect):
    import time
    import random

    n = 10
    total = 400

    # Smart Insert
    User.objects.delete()

    users = set([User(user_id=random.randint(1, total)) for i in range(n)])
    User.objects.insert(users)
    assert int(0.5 * n) <= User.objects.count() <= n

    users = [User(user_id=i) for i in range(1, 1 + total)]

    st = time.clock()
    User.smart_insert(users)
    elapse1 = time.clock() - st

    assert User.objects.count() == total  # after smart insert, we got 400 doc

    # Regular Insert
    User.objects.delete()

    users = set([User(user_id=random.randint(1, total)) for i in range(n)])
    User.objects.insert(users)
    assert int(0.5 * n) <= User.objects.count() <= n

    users = [User(user_id=i) for i in range(1, 1 + total)]

    st = time.clock()
    for user in users:
        try:
            user.save()
        except:
            pass
    elapse2 = time.clock() - st

    assert User.objects.count() == total  # after regular insert, we got 400 doc

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
