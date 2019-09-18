# -*- coding: utf-8 -*-

import sys
import pytest
import mongoengine


@pytest.fixture
def connect():
    # just a test mongodb in container
    dbname = "devtest"
    username = "admin"
    password = "&2z7#tMH6BJt"
    host = "mongodb://{username}:{password}@ds113063.mlab.com:13063/devtest".\
        format(username=username, password=password)
    client = mongoengine.connect(
        dbname,
        host=host,
        retryWrites=False,
    )
    db = client[dbname]

    py_ver = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
    for col_name in db.list_collection_names():
        if col_name.endswith(py_ver):
            db[col_name].remove({})
