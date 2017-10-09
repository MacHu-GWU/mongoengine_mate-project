#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mongoengine


@pytest.fixture
def connect():
    dbname = "devtest"
    username = "admin"
    password = "&2z7#tMH6BJt"
    host = "mongodb://{username}:{password}@ds113063.mlab.com:13063/devtest".\
        format(username=username, password=password)
    conn = mongoengine.connect(
        dbname,
        host=host,
    )
    conn.drop_database(dbname)
