# -*- coding: utf-8 -*-

import pytest

import sys
import random
from sfm.timer import DateTimeTimer
import mongoengine
from mongoengine_mate import ExtendedDocument

py_ver = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
user_col_name = "user_%s" % py_ver


class User(ExtendedDocument):
    _id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()
    dob = mongoengine.StringField()

    meta = {
        "collection": user_col_name
    }


def test_smart_update_correctness(connect):
    # single document
    User.objects.delete()

    User(_id=1, name="Alice").save()
    User.smart_update(User(_id=2, name="Bob"), upsert=False)
    assert User.objects.count() == 1

    User.smart_update(User(_id=2, name="Bob"), upsert=True)
    assert User.objects.count() == 2

    User.smart_update(User(_id=1, dob="1990-01-01"))
    assert User.objects(_id=1).get().dob == "1990-01-01"

    # batch update
    User.objects.delete()

    User.objects.insert(User(_id=2, name="Bob", dob="1990-01-01"))

    # upsert = False
    data = [
        User(_id=1, name="Alice"),
        User(_id=2, name="Bryan"),
        User(_id=3, name="Cathy"),
    ]
    User.smart_update(data, upsert=False)
    assert User.objects.count() == 1
    assert [
        obj.to_dict()
        for obj in User.objects()
    ] == [
        {"_id": 2, "name": "Bryan", "dob": "1990-01-01"},
    ]

    # upsert = True
    data = [
        User(_id=1, name="Alice"),
        User(_id=2, name="Bruce"),
        User(_id=3, name="Cathy"),
    ]
    User.smart_update(data, upsert=True)

    assert User.objects.count() == 3
    assert [
        obj.to_dict()
        for obj in User.objects()
    ] == [
        {"_id": 2, "name": "Bruce", "dob": "1990-01-01"},
        {"_id": 1, "name": "Alice", "dob": None},
        {"_id": 3, "name": "Cathy", "dob": None},
    ]


def test_smart_update_performance(connect):
    n_total = 100
    n_breaker = 25

    total_user_ids = list(range(1, 1 + n_total))
    random.shuffle(total_user_ids)
    breaker_user_ids = total_user_ids[:n_breaker]

    User.objects.delete()
    total_users = [User(_id=_id, name="Bob") for _id in total_user_ids]
    breaker_users = [User(_id=_id, name="Alice") for _id in breaker_user_ids]

    User.smart_insert(breaker_users)
    assert User.objects.count() == n_breaker
    with DateTimeTimer(title="just upsert"):
        User.smart_update(total_users, upsert=True, _insert_after_update=False)
    assert User.objects.count() == n_total

    # insert_after_update strategy
    User.objects.delete()
    total_users = [User(_id=_id, name="Bob") for _id in total_user_ids]
    breaker_users = [User(_id=_id, name="Alice") for _id in breaker_user_ids]

    User.smart_insert(breaker_users)
    assert User.objects.count() == n_breaker
    with DateTimeTimer(title="insert after update"):
        User.smart_update(total_users, upsert=True, _insert_after_update=True)
    assert User.objects.count() == n_total


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
