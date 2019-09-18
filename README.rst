
.. image:: https://readthedocs.org/projects/mongoengine_mate/badge/?version=latest
    :target: https://mongoengine_mate.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://travis-ci.org/MacHu-GWU/mongoengine_mate-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/mongoengine_mate-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/mongoengine_mate-project/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MacHu-GWU/mongoengine_mate-project

.. image:: https://img.shields.io/pypi/v/mongoengine_mate.svg
    :target: https://pypi.python.org/pypi/mongoengine_mate

.. image:: https://img.shields.io/pypi/l/mongoengine_mate.svg
    :target: https://pypi.python.org/pypi/mongoengine_mate

.. image:: https://img.shields.io/pypi/pyversions/mongoengine_mate.svg
    :target: https://pypi.python.org/pypi/mongoengine_mate

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/mongoengine_mate-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
      :target: https://mongoengine_mate.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
      :target: https://mongoengine_mate.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
      :target: https://mongoengine_mate.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
      :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/mongoengine_mate-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
      :target: https://github.com/MacHu-GWU/mongoengine_mate-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
      :target: https://github.com/MacHu-GWU/mongoengine_mate-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.org/pypi/mongoengine_mate#files


Welcome to ``mongoengine_mate`` Documentation
==============================================================================

``mongoengine_mate`` includes lots more utility method in ORM model Class, makes ``mongoengine`` more powerful.


Usage
------------------------------------------------------------------------------

.. code-block:: python

    import mongoengine
    from mongoengine_mate import ExtendedDocument

    class User(ExtendedDocument):
        id = mongoengine.IntField()
        name = mongoengine.StringField()


First, you got better ``__repr__()`` like:

.. code-block:: python

    >>> User(id=1, name="Alice")
    User(id=1, name="Alice")

    # access its collection or database
    >>> col_user = User.col()
    >>> col_user.find({"_id": 1})
    >>> col_db = User.db()

    # access its field name in order
    >>> User.fields_ordered()
    ["id", "name"]

    # provide dictionary-like api
    >>> user = User(id=1, name="Alice")
    >>> user.keys()
    ["id", "name"]

    >>> user.values()
    [1, "Alice"]

    >>> user.items()
    [("id", "name"), (1, "Alice")]

    >>> user.to_dict()
    {"id": 1, "name": "Alice"}

    >>> user.to_OrderedDict()
    OrderedDict([("id", "name"), (1, "Alice")])


Smart Insert - Skip Primary Key Conflict
------------------------------------------------------------------------------

When you do batch insert, sometimes one or a few documents may cause ``_id`` field conflict error, which is breaking the batch insert operation.

Usually you have to write a ``for loop` and use ``try ... except ...`` to ignore conflict. But, it is SLOW!

``ExtendedDocument.smart_insert`` provides a fast and convenient way to batch insert lots of document at once correctly.

.. code-block:: python

    # insert one document which breaks the batch insert
    User(id=100, name="Obama").save()

    # smart_insert, automatically handle NotUniqueError
    User.smart_insert([
        User(id=1, name="Alice"),
        User(id=2, name="Bob"),
        ...
        User(id=1000, name="Zillow"),
    ])


Smart Update - Batch Upsert
------------------------------------------------------------------------------

When you do batch update, you mostly want to use the ``_id`` field to locate which document you want to update.

.. code-block:: python

    >>>User(id=2, name="Bob").save()

    # update only
    >>> User.smart_update([
        User(id=1, name="Alice"),
        User(id=2, name="Bruce"),
        User(id=3, name="Cathy"),
    ], upsert=False)
    >>> User.objects.count()
    1

    # upsert
    >>> User.smart_update([
        User(id=1, name="Alice"),
        User(id=2, name="Bruce"),
        User(id=3, name="Cathy"),
    ], upsert=True)
    >>> User.objects.count()
    3


.. _install:

Install
------------------------------------------------------------------------------

``mongoengine_mate`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install mongoengine_mate

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade mongoengine_mate