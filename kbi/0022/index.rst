.. index::
   single: datalad save; git mv

KBI0022: Performance of ``mv`` + ``datalad save`` vs ``git mv`` + ``git commit``  when renaming dataset directories 
===================================================================================================================

:authors: Stephan Heunis <jsheunis@gmail.com>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/issues/74
:keywords: performance, time, datalad save, mv, git move, rename
:software-versions: datalad_0.18.4, git-annex_10.20230330-g98a3ba0ea

When renaming a directory that contains many files in DataLad dataset,
a subsequent ``datalad save`` may take an unexpected amount of time. While performance
is always relative, it is worth considering the use of ``git mv`` followed by
``git commit`` instead of a standard ``mv`` and ``datalad save`` in datasets with large
trees.

.. note::

   The use of ``mv`` for renaming and moving dataset content is covered extensively
   in a dedicated DataLad Handbook chapter: `Miscellaneous file system operations`_.
   This also includes comparisons with ``git mv`` and comments on when and when not to
   use either of these methods. Performance, however, is not covered in the handbook
   and is hence presented here.
   **Important:** The recommendations here solely apply to directories. ``git mv`` operations should `not be performed on subdatasets <https://github.com/datalad/datalad/issues/3464>`_. Instead, stick to a plain ``mv`` followed by a ``datalad save``. 

.. _Miscellaneous file system operations: https://handbook.datalad.org/en/latest/basics/101-136-filesystem.html

A simple performance comparison
-------------------------------

The following test was done on a Macbook Pro. Let's say we start off with a simple
dataset with the following structure:

.. code-block:: console

   >> tree ../test_dataset
   
   ../test_dataset
   └── toplevel
      ├── A
      │   ├── one
      │   │   └── a1.txt
      │   └── two
      │       └── a2.txt
      └── B
         ├── one
         │   └── b1.txt
         └── two
               └── b2.txt

To rename the directory ``toplevel``, we can follow one of two options:

``mv`` and ``datalad save``
+++++++++++++++++++++++++++

.. code-block:: console

   >> time ( mv toplevel new_toplevel; datalad save )

   add(ok): new_toplevel/A/one/a1.txt (file)
   add(ok): new_toplevel/A/two/a2.txt (file)
   add(ok): new_toplevel/B/one/b1.txt (file)
   add(ok): new_toplevel/B/two/b2.txt (file)
   save(ok): . (dataset)
   action summary:
   add (ok: 4)
   save (ok: 1)
   ( mv toplevel new_toplevel; datalad save; )  0.41s user 0.39s system 85% cpu 0.933 total


``git mv`` and ``git commit``
+++++++++++++++++++++++++++++

.. note::

   `git mv`_ encapsulates a ``mv`` operation from the old path to the new path, 
   followed by staging the new path, and removing the old path. This implies
   that it is not necessary to run a ``git add`` on the new path after a ``git mv``,
   the path can just be committed.

.. _git mv: https://git-scm.com/docs/git-mv

.. code-block:: console

   >> time ( git mv toplevel new_toplevel; git commit -m "rename directory" )

   [main ee82fde] rename directory
   4 files changed, 0 insertions(+), 0 deletions(-)
   rename {toplevel => new_toplevel}/A/one/a1.txt (100%)
   rename {toplevel => new_toplevel}/A/two/a2.txt (100%)
   rename {toplevel => new_toplevel}/B/one/b1.txt (100%)
   rename {toplevel => new_toplevel}/B/two/b2.txt (100%)
   ( git mv toplevel new_toplevel; git commit -m "rename directory"; )  0.03s user 0.05s system 70% cpu 0.117 total

Summary
+++++++

As you can see, the ``mv`` + ``datalad save`` option took about 1 second while the ``git mv``
+ ``git commit`` option was about 8 times faster. While this is not substantial on a small scale,
it could be an important consideration when renaming paths in datasets with large
filetrees. Importantly, this point is purely about performance and does not
consider other aspects that could influence the decision of which renaming method
to use.