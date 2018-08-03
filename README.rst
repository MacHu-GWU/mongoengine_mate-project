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

.. image:: https://img.shields.io/badge/Star_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/mongoengine_mate-project


Welcome to ``mongoengine_mate`` Documentation
==============================================================================

``mongoengine_mate`` is a library extend power of `mongoengine <http://docs.mongoengine.org>`_


Quick Links
------------------------------------------------------------------------------
- .. image:: https://img.shields.io/badge/Link-Document-red.svg
      :target: https://mongoengine_mate.readthedocs.io/index.html

- .. image:: https://img.shields.io/badge/Link-API_Reference_and_Source_Code-red.svg
      :target: https://mongoengine_mate.readthedocs.io/py-modindex.html

- .. image:: https://img.shields.io/badge/Link-Install-red.svg
      :target: `install`_

- .. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/mongoengine_mate-project

- .. image:: https://img.shields.io/badge/Link-Submit_Issue_and_Feature_Request-blue.svg
      :target: https://github.com/MacHu-GWU/mongoengine_mate-project/issues

- .. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.python.org/pypi/mongoengine_mate#downloads


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


Then, you got more built-in method to do:

.. code-block:: python

    # smart_insert, automatically handle NotUniqueError
    User.smart_insert([
        User(id=1, name="Alice"),
        User(id=2, name="Bob"),
    ])

    # access its collection or database
    col_user = User.col()
    col_db = User.db()

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


More examples can be found at https://github.com/MacHu-GWU/mongoengine_mate-project/blob/master/mongoengine_mate/document.py


.. _install:

Install
------------------------------------------------------------------------------

``mongoengine_mate`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install mongoengine_mate

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade mongoengine_mate
