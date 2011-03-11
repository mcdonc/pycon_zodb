ZODB: A Python Persistence System
=================================

:Authors: Chris McDonough, Agendaless Consulting
:Date: 3/11/2011 (PyCon 2011)

..  footer:: Chris McDonough, Agendaless Consulting

What Is ZODB?
-------------

- ZODB == Zope Object Database.  Independent of Zope-the-web-framework.

- "Suspend for Python": use Python objects like you would normally.  When you
  shut your process down and bring it back up, your objects will magically be
  in the state they were when you last shut down.

- Useful where you might use another embedded database (SQLite), but also
  includes a server component for multiprocess applications.

- BSD-ish license.

The Pickle Module
-----------------

``pickle`` is a module for serializing Python object state to files.  A
pickleable object:

.. sourcecode:: python

    class Conference(object):
        def __init__(self, name, year):
            self.name = name
            self.year = year
        def title(self):
            return self.name.capitalize()

Writing Data to a Pickle File
-----------------------------

.. sourcecode:: python

    from pickle import dump
    pycon = Conference('pycon', 2011)
    print pycon.title(), pycon.year # Pycon 2011
    f = open('data.pck', 'wb')
    pycon = dump(pycon, f)
    
Reading Data from a Pickle File
-------------------------------

.. sourcecode:: python

    from pickle import load
    f = open('data.pck', 'rb')
    pycon = load(f)
    print pycon.title(), pycon.year

Modifying Data in A Pickle File
-------------------------------

.. sourcecode:: python

    from pickle import load, dump
    f = open('data.pck', 'rb')
    pycon = load(f)
    print pycon.title(), pycon.year
    pycon.year = 2012
    out = open('data.pck', 'wb')
    dump(pycon, out)
    
The Pickle Format
-----------------

Printable ASCII format (can also be binary).

::

    [chrism@thinko pycon]$ cat data.pck 
    ccopy_reg
    _reconstructor
    p0
    (c__main__
    Conference
    p1
    c__builtin__
    ...

Pickle Limitations
------------------

- Can't be read or modified by anything other than a Python interpreter.

- Loading an "untrusted" pickle is a security risk.

- Not all Python types can be pickled (anything that deals with interpreter
  state cannot be pickled: a generator, a file handle).

- Pickles refer to custom classes by fully qualified name,
  e.g. ``myproject.mymodule.MyClass``.  Seaver's Law: "Persistence means
  always having to say you're sorry".

Pickleable Types
----------------

- ``None``, ``True``, and ``False``.

- Integers, longs, floats, complex numbers.

- Tuples, lists, sets, dictionaries containing pickleable objects.

- Functions and classes defined at the top level of a module.

- Instances of classes (where the class is defined at module scope) which has
  a pickleable ``__dict__`` or a suitable ``__setstate__``.

Replacing Pickle With ZODB
--------------------------

- Same limitations as ``pickle`` described previously.

- Persistent objects subclass ``persistent.Persistent``.

- Each persistent object is sort of like a row in a SQL database.

- ZODB actually uses the ``pickle`` module under the hood.

ZODB Features Beyond Pickle
---------------------------

- Manages the object working set so it can be larger than available RAM.

- Tracks discrete object changes rather than requiring the persistent state
  of the entire working set to be rewritten completely.

- Writes are transactional.

Declaring a Persistent Object
-----------------------------

.. sourcecode:: python

    from persistent import Persistent

    class Conference(Persistent):
        def __init__(self, name, year):
            self.name = name
            self.year = year
        def title(self):
            return self.name.capitalize()

Writing Data to a ZODB
----------------------

.. sourcecode:: python

    import transaction
    from ZODB.FileStorage import FileStorage
    from ZODB.DB import DB
    fs = FileStorage('data.fs')
    db = DB(fs)
    conn = db.open()
    root = conn.root()
    pycon = Conference('pycon', 2011)
    print pycon.title(), pycon.year
    root['pycon'] = pycon
    transaction.commit()

Reading Data from a ZODB
------------------------

.. sourcecode:: python

    from ZODB.FileStorage import FileStorage
    from ZODB.DB import DB
    fs = FileStorage('data.fs')
    db = DB(fs)
    conn = db.open()
    root = conn.root()
    pycon = root['pycon']
    print pycon.title()

Modifying ZODB Data
-------------------

.. sourcecode:: python

    import transaction
    from ZODB.FileStorage import FileStorage
    from ZODB.DB import DB
    fs = FileStorage('data.fs')
    db = DB(fs)
    conn = db.open()
    root = conn.root()
    pycon = root['pycon']
    pycon.year = 2012
    transaction.commit()

Transactionality
----------------

- Transactions are bounded by calls to ``transaction.commit()``.

- ZODB implements "snapshot" isolation level with respect to competing
  transactions.  All reads during a transaction see the data in the database
  at the time that the transaction began.

- The ``transaction`` module can supply two-phase commit synchronization
  between multiple persistence systems (keep ZODB data in sync with data in a
  relational database, for example).
    
ZODB History
------------

- 1998-1999: BoboPOS.  Single threaded, single-process embedded only.

- 2000-2001: ZODB, multi-threaded, single-process embedded only.

- 2001-present: ZODB with ZEO means multiprocess access.

- Current version: 3.10.X

ZODB vs. "Database"
-------------------

- Misnomer: ZODB really should not be called a "database", as it invites
  unwelcome comparisons. 

- Should instead really be called ZOPS (Z Object Persistence System) or
  "superpickle".

ZODB vs. "Database" (cont'd)
----------------------------

- ZODB doesn't have a declarative, structured query language (Python is
  the query language).

- ZODB doesn't have a database-level indexing system (indices are presumed to
  be an application-level feature, not a database feature).

- A ZODB cannot be queried from processes that are not Python without an
  intermediary (like a web service).

Object Databases
----------------

- The most famous object database: the Smalltalk ``image``.

- ZODB is as close as Python will ever get to having a similar feature.

ZODB vs. relational databases
-----------------------------

- Not "relational" by any definition that an application programmer might
  use.

- Relationships are created via Python object references and by
  indexing/querying systems built on top of ZODB.

- No schema; no mapping of types.  WYSIWYG.

ZODB vs. NoSQL databases
------------------------

- NoSQL databases are usually not tied to a particular language.  ZODB is
  tied to Python.

- Often used as a "graph database", although this moniker isn't really
  completely accurate either.  It's an object database.  It's just having
  Python objects that stick around longer than a single process run.

- No indexing, no query language other than Python, etc.

Folders
-------

- Folders are data structures which provide efficient storage for large
  collections of subobjects.

- Can store millions of persistent objects without undue memory consumption
  or pickling inefficency.  Based on persistent BTrees.

Folders (cont'd)
----------------

.. sourcecode:: python

    from persistent import Persistent
    from repoze.folder import Folder
    import transaction
    from ZODB.FileStorage import FileStorage
    from ZODB.DB import DB
    fs = FileStorage('data.fs')
    db = DB(fs)
    conn = db.open()
    folder = Folder()
    root = conn.root()
    root['folder'] = folder

Folders (cont'd)
----------------

.. sourcecode:: python

    pycon = Conference('pycon', 2011)
    folder['pycon'] = pycon
    print pycon.title(), pycon.year
    transaction.commit()

Storage Types
-------------

- FileStorage: stores pickles in a single file (default).

- DirectoryStorage: stores pickles in directories.

- RelStorage: stores pickles in relational database tables.

- MappingStorage: stores pickles in memory.

Using Alternate Storages
------------------------

.. sourcecode:: python

    import transaction
    from ZODB.MappingStorage import MappingStorage
    from ZODB.DB import DB
    fs = MappingStorage()
    db = DB(fs)

Scaling across multiple clients
-------------------------------

Use a server process to scale across multiple clients.

- ZEO uses a custom server process.

- RelStorage uses a relational database process.

Indexing and Searching
----------------------

- ``repoze.catalog`` provides indexes and a query language.

- Index types: ``Field``, ``Text``, ``Path``, ``Keyword``, and ``Facet``.

- Text index is a full text indexing and query system.

Catalog Setup (Discriminators)
------------------------------

.. sourcecode:: python

   def get_flavor(object, default):
       return getattr(object, 'flavor', default)

   def get_text(object, default):
       return getattr(object, 'text', default)

Catalog Setup (cont'd)
----------------------

.. sourcecode:: python

   from repoze.catalog.indexes.field import \
          CatalogFieldIndex
   from repoze.catalog.indexes.text import \
          CatalogTextIndex
   from repoze.catalog.catalog import Catalog

   catalog = Catalog()
   catalog['flavors'] = CatalogFieldIndex(get_flavor)
   catalog['text'] = CatalogTextIndex(get_text)

   root['catalog'] = catalog

Indexing
--------

.. sourcecode:: python

  class IceCream(object):
      def __init__(self, flavor, description):
          self.flavor = flavor
          self.description = description

  peach = IceCream('peach', 
                   'Has a peachy flavor')
  catalog.index_doc(1, peach)

  pistachio = IceCream('pistachio',
                       'Tastes like pistachio nuts')
  catalog.index_doc(2, pistachio)
   
Querying
--------

.. sourcecode:: python

   from repoze.catalog.query import Eq

   numdocs, results = catalog.query(
       Eq('flavors', 'peach') & Eq('text', 'nutty')
       )

   print (numdocs, [ x for x in results ])

Scaling
-------

- No practical limit to storage size.

- No sharding solution (except a manual one using multiple databases).

- Server can be a single point of failure without ZRS/ZeoRAID or RelStorage.

- ZODB has built-in "blobs" making it possible to store and retrieve large
  binary objects efficiently.

Unique ZODB Features
--------------------

- Undo.

- Time travel.

- BLOBs.

Limitations
-----------

- Has C components; won't run under anything but CPython (yet?).

- Python-only.

- Schemaless != no evolution.  Evolution is still a problem with ZODB
  applications (and any application with persistent data).

Conclusion
----------

- ZODB is an excellent choice for an embedded persistence system in any
  Python application.

- ZODB is a poor choice if you expect it to be a relational database or for
  it to provide inherent indexing and querying features without additional
  software.

- ZODB may be a poor choice if you expect lots of concurrent writes.

