# -*- coding: utf-8 -*-

import pytest

import sys
from pymongo.database import Database
import mongoengine
from mongoengine_mate import ExtendedDocument

py_ver = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
user_col_name = "user_%s" % py_ver


class User(ExtendedDocument):
    user_id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()

    meta = {
        "collection": user_col_name
    }


def test_smart_insert(connect):
    import time
    import random

    n_breaker = 5
    n_total = 120

    # Smart Insert
    User.objects.delete()

    total_user_ids = list(range(1, 1+n_total))
    random.shuffle(total_user_ids)
    breaker_user_ids = total_user_ids[:n_breaker]

    total_users = [User(user_id=_id) for _id in total_user_ids]
    breaker_users = [User(user_id=_id) for _id in breaker_user_ids]

    User.objects.insert(breaker_users)
    assert User.objects.count() == n_breaker

    st = time.clock()
    n_insert, n_skipped = User.smart_insert(total_users)
    elapse1 = time.clock() - st
    assert n_insert == n_total - n_breaker
    assert n_skipped == n_breaker
    assert User.objects.count() == n_total  # after smart insert, we got 400 doc
    assert [
        user.to_dict()
        for user in User.objects
    ] == [
        user.to_dict()
        for user in total_users
    ]

    # Regular Insert
    User.objects.delete()

    total_users = [User(user_id=_id) for _id in total_user_ids]
    breaker_users = [User(user_id=_id) for _id in breaker_user_ids]

    User.objects.insert(breaker_users)
    assert User.objects.count() == n_breaker

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


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
