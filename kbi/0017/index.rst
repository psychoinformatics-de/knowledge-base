.. index::
   single: <topic>; <subtopic>

KBI0017: How to delete commits includling their annexed data
============================================================

:authors: Christian Mönch <christian.moench@web.de>
:discussion: <link>
:keywords: delete commits, delete annexed data
:software-versions: datalad_0.8.13, git-annex_10.20230407

This knowledge base item describes how to delete commits and
the annexed data that was added to the annex when the commits
were created.


The initial state and the goal
------------------------------

There is a datalad dataset with an annex and a number of commits.
Some of those commits added files to the annex, and some might
just have added files to git. We assume that the last commit has
added a number of files to the annex.

The goal is to remove the last commit and all annexed files that
were added when the commit was performed.


Principal strategy
------------------

To remove a commit and all annexed files, two phases have to be
executed. First, the commit itself has to be removed. Second, the
annexed files that were added in the commit, and moved into the
annex object store have to be removed.

There are a few ways to delete commits from git. We propose to
use an interactive `git rebase`. Let's assume the git-log looks
like this:

.. code-block:: bash

    255c4fd (HEAD -> master) add two more files
    9bb8847 add two initial files
    2dd6618 [DATALAD] new dataset

To remove the last commit, first execute a rebase onto the
hash that preceeds the last commit, i.e. ``9bb8847``. To do
that execute the command:

.. code-block:: bash

    git rebase -i 9bb8847

During the interactive rebase drop commit ``255c4fd``.
(It is possible to drop multiple commits in a single interactive
git rebase by choosing another commit as a rebase target.)

Now the links to the annexed content are removed. In order
to remove the annex content itself, execute the command:

.. code-block:: bash

    git annex unused

That will display a number of annexed files that are now
unused. For example:

.. code-block:: bash

    unused . (checking for unused data...) (checking master...)
      Some annexed data is no longer used by any files:
        NUMBER  KEY
        1       MD5E-s9--c31ea01ca12b5558b6503a8143cdb98c.txt
        2       MD5E-s11--1d6f4be608158f767aafd1bab92043a7.txt

The unused files can now be dropped with the command ``git annex
dropunused``:

.. code-block:: bash

    > git annex dropunused 1
    > git annex dropunused 2


Words of warning
----------------

Not every presently "unused" key might be from a delete commit. There might be
other historical data that is also no longer referenced, but still useful.

BE CAREFUL!

One useful approach is to have a branch or tag on everything that is important
-- ``git annex unused`` would then consider those objects necessary.
``git annex unused`` is quite powerful, we recommend studying the help for it.
