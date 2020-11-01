.. _apiref:

API Reference
=============

Sqlfluff exposes a public api for other python applications to use.
A basic example of this usage is given here, with the documentation
for each of the methods below.


.. literalinclude:: ../../examples/basic_api_usage.py
   :language: python


Simple API commands
-------------------


.. automodule:: sqlfluff
   :members: lint, fix, parse


Advanced API usage
------------------

The simple API presents only a fraction of the functionality present
within the core sqlfluff library. For more advanced use cases, users
can import the :code:`Linter()` and :code:`FluffConfig()` classes from
:code:`sqlfluff.core`. As of version 0.4.0 this is considered as
*experimental only* as the internals may change without warning in any
future release. If you come to rely on the internals of sqlfluff, please
post an issue on github to share what you're up to. This will help shape
a more reliable, tidy and well documented public API for use.
