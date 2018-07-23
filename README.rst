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

Usage::

    import mongoengine
    from mongoengine_mate import ExtendedDocument

    class User(ExtendedDocument):
        id = mongoengine.IntField()
        name = mongoengine.StringField()


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


.. _install:

Install
------------------------------------------------------------------------------

``mongoengine_mate`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install mongoengine_mate

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade mongoengine_mate
