.. index::
   single: datalad push; git annex sync

KBI0015: ``datalad push`` vs ``git annex sync``
===============================================

:authors: Stephan Heunis <jsheunis@gmail.com>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/64
:keywords: datalad push, git annex sync
:software-versions: datalad_0.18.3, git_2.39.1

This Knowledge Base Item outlines the differences and similarities between `datalad push`_
and `git annex sync`_.

.. _datalad push: https://handbook.datalad.org/en/latest/basics/101-141-push.html
.. _git annex sync: https://git-annex.branchable.com/sync/

Question:
---------

**Is ``git annex sync`` the equivalent of ``datalad push``?**

Answer:
-------

In short: No, these commands are not equivalent.

``git annex sync`` synchronizes the states of a local repository and its remotes,
which includes:

   "...first committing any local changes to files that have previously been added to the
   repository, then fetching and merging the current branch and the git-annex branch from
   the remote repositories, and finally pushing the changes back to those branches on the
   remote repositories."

In git terms, this involves ``fetch``, ``merge``, and ``push`` operations between linked 
repositories. By default, ``git annex sync`` only syncs git branches and not the annexed
data, although this behavior can be changed with the ``--content`` flag or the
``annex.synccontent`` configuration.

``datalad push``, on the other hand, does not involve this bi-directional process of
updating repositories. Instead, it literally just pushes local updates in a DataLad
dataset to a remote sibling. Under the hood, the ``datalad push`` command uses
``git push`` and ``git annex copy`` to push a dataset.

A somewhat more relevant datalad command compared to ``git annex sync`` would be
`datalad update`_, which is used to fetch and optionally merge updates from a sibling into
a DataLad dataset.

.. _datalad update: https://docs.datalad.org/en/stable/generated/man/datalad-update.html