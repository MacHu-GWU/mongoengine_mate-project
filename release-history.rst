.. _release_history:

Release and Version History
==============================================================================


0.0.6 (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.0.5 (2019-12-27)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

- now ``mongoengine_mate.ExtendedDocument.absorb()`` and ``mongoengine_mate.ExtendedDocument.revise()`` returns the data been changed as a dictionary.

**Bugfixes**

- use ``(mongoengine.NotUniqueError, mongoengine.BulkWriteError)`` instead ``mongoengine.NotUniqueError`` if possible in newer ``pymongo`` version.

**Miscellaneous**

- drop support for Python3.4 and Python3.5


0.0.1 (2019-09-17)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- First release