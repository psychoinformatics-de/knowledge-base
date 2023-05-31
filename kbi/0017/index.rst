.. index::
   single: delete; commits & data

KBI0017: How to delete commits including their annexed data
===========================================================

:authors: Christian Mönch <christian.moench@web.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/69
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
added a number of files to the annex. The dataset has not yet been
pushed to a sibling.

The goal is to remove the last commit and all annexed files that
were added when the commit was performed. (However, the same process
can be applied for any specific commit, not only the last. See the `note`_
below.)


Principal strategy
------------------

To remove a commit and all annexed files, two phases have to be
executed. First, the commit itself has to be removed. Second, the
annexed files that were added in the commit, and moved into the
annex object store, have to be removed.

There are a few ways to delete commits from git. We propose to
use an interactive `git rebase`_.

.. _note:

.. note::

    Technically, a ``git reset --hard`` could also be used in this instance
    to reset the current branch tip to the specific commit before the last.
    However, let's suppose that the single commit that we wanted to remove
    was not the last one, and that other commits that we consider useful were
    added after the to-be-removed commit. We wouldn't want to remove those
    other commits as well, which is exactly what a ``git reset --hard`` would
    do if it was applied to the commit preceding the to-be-removed commit.
    In this case, ``git reset --hard`` provides much more flexibility to pick
    and drop specific commits, as demonstrated below.

Let's assume the git-log looks like this:

.. code-block:: bash

    255c4fd (HEAD -> master) add two more files
    9bb8847 add two initial files
    2dd6618 [DATALAD] new dataset

To remove the last commit, first execute a rebase onto the
hash that precedes the last commit, i.e. ``9bb8847``. To do
that execute the command:

.. code-block:: bash

    git rebase -i 9bb8847

During the interactive rebase drop commit ``255c4fd``.
(It is possible to drop multiple commits in a single interactive
git rebase by choosing another commit as a rebase target.)

Now the links to the annexed content are removed. In order
to remove the annex content itself, execute the command `git annex unused`_:

.. code-block:: bash

    git annex unused

That will display a number of annexed files that are not
referenced anymore from git. For example:

.. code-block::

    unused . (checking for unused data...) (checking master...)
      Some annexed data is no longer used by any files:
        NUMBER  KEY
        1       MD5E-s9--c31ea01ca12b5558b6503a8143cdb98c.txt
        2       MD5E-s11--1d6f4be608158f767aafd1bab92043a7.txt
   (To see where this data was previously used, run: git annex whereused --historical --unused

The result provides the numbers that can be used to drop the annexed data,
here `1` and `2`. The result does not tell us much about the data that is
unused. It is important to note, that not every unused data need to be
from the deleted commit. There might be other historical data that is also
no longer referenced, but still useful. Git-annex provides a command to
examine the unused data more closely: `git annex whereused --historical --unused`:

.. code-block::

    > git annex whereused --historical --unused
    MD5E-s9--c31ea01ca12b5558b6503a8143cdb98c.txt HEAD@{2}:./file_1.txt
    MD5E-s11--1d6f4be608158f767aafd1bab92043a7.txt HEAD@{2}:./file_2.txt

The output can be used to determine two things. First, which file name is
associated with a key. Second, we can find the commits that created the data
objects, that are now unused. The output `HEAD@{2}` refers to an entry in git's
reflog. It can be examined with the command `git reflog`:

.. code-block::

    > git reflog
    0fbb9e2 (HEAD -> master) HEAD@{0}: commit: add more files
    6e56f3d HEAD@{1}: reset: moving to 6e56f3d2c628476d8af0c2d1d14f3e4b560f017f
    5a498f9 HEAD@{2}: commit: save files for subject 1 and subject 2
    ...

The commit message, here: `save files for subject 1 and subject 2` and the
gitsha of the commit, here: `5a498f9` allow to investigate in more detail
what data is contained in the data-objects.

Another option to determine whether the data object is still of value is of
course to examine the data object itself.

Once a file has been identified as really unused, it can be dropped with
the command `git annex dropunused`_:

.. code-block:: bash

    > git annex dropunused 1
    > git annex dropunused 2



.. _git rebase: https://git-scm.com/docs/git-rebase
.. _git annex unused: https://git-annex.branchable.com/git-annex-unused/
.. _git annex dropunused: https://git-annex.branchable.com/git-annex-dropunused/

Words of warning
----------------

Despite the described processes to determine the value of an unused file, there
is still the risk to delete an "unused" data object, that was actually still of
value.

BE CAREFUL!

One useful approach is to have a branch or tag on everything that is important
-- ``git annex unused`` would then consider those objects necessary.
``git annex unused`` is quite powerful, we recommend studying the help for it.
