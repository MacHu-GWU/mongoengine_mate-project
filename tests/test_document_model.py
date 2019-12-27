# -*- coding: utf-8 -*-

import pytest
from pytest import raises

import mongoengine
from mongoengine_mate import ExtendedDocument


class User(ExtendedDocument):
    user_id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()


class Item(ExtendedDocument):
    _id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()


# --- Data Model ---
def test_id_field_name(connect):
    assert User.id_field_name() == "user_id"
    assert Item.id_field_name() == "_id"


def test_fields_ordered(connect):
    assert User.fields_ordered() == ["user_id", "name"]


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
    assert user.to_dict(include_none=True) == {"user_id": 1, "name": "Jack"}
    assert user.to_dict(include_none=False) == {"user_id": 1, "name": "Jack"}
    assert user.to_OrderedDict(include_none=True) == {
        "user_id": 1, "name": "Jack"}
    assert user.to_OrderedDict(include_none=False) == {
        "user_id": 1, "name": "Jack"}

    assert user.to_json() == '{"_id": 1, "name": "Jack"}'


def test_absorb(connect):
    user = User(id=1, name="Jack")
    overwritten_data = user.absorb(User(name="Tom"))
    assert user.name == "Tom"
    assert overwritten_data == {"name": "Tom"}

    with raises(TypeError):
        user.absorb({"name": "Tom"})

    class MyClass(object):
        pass

    with raises(TypeError):
        user.absorb(MyClass())


def test_revise(connect):
    user = User(id=1, name="Jack")
    user_data = {"name": "Tom"}
    overwritten_data = user.revise(user_data)
    assert user.name == "Tom"
    assert overwritten_data == {"name": "Tom"}

    with raises(TypeError):
        user.revise([("name", "Tome")])


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
