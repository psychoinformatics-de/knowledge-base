.. index::
   single: special remote; reconfigure
   single: git-annex; git special remote

.. highlight:: console

KBI0006: How to fix-up a git-type special remote with a new location
====================================================================

:authors: Adina Wagner <adina.wagner@t-online.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/22
:keywords: special remote, git-annex, gitannex; enableremote

In many datasets, special remotes ensure that annexed file content can
be retrieved from external sources.
Sometimes, however, external resources vanish.
This happened to data of the studyforrest project:
Initially, data was hosted on University of Magdeburg's
infrastructure (``psydata.ovgu.de``), and registered as a `Git-type special remote`_
``mddatasrc``:

.. code-block:: console

   $ git cat-file -p git-annex:remote.log
   9536f86d-eb34-42ed-8ffc-fafd63a2b87e autoenable=true location=http://psydata.ovgu.de/studyforrest/visualrois/.git name=mddatasrc type=git timestamp=1459405007.225384s
   [...]

This means that the webserver behind ``psydata.ovgu.de`` contains a publicly accessible
annex repo with all file content.
When the group moved institutions, the data was migrated to the new institution's
hosting infrastructure.
The former URL was configured to redirect to this new data source.
This kept data retrieval functional for a few years.
However, ``psydata.ovgu.de`` was eventually taken down by the former institution.
This made data retrieval impossible, and led to delays in the dataset, since any
git-annex operations tried to contact the special remote until it timed out.

.. _Git-type special remote: https://git-annex.branchable.com/special_remotes/git

How to update location information of the special remote
--------------------------------------------------------

The procedure to update the special remote was two-fold:

The problematic dataset was cloned from GitHub, its central entrypoint, to apply the fix.
First, the corresponding Git remote was removed:

.. code-block:: bash

   $ git remote remove mddatasrc

Next, it was possible to update the special remote by re-enabling it with updated location information.
This command required knowledge of the new hosting location (again a publicly accessible
annex repo), and the UUID of the special remote, taken from ``remote.log``::

   $ git annex enableremote 9536f86d-eb34-42ed-8ffc-fafd63a2b87e   location=https://datapub.fz-juelich.de/studyforrest/studyforrest/visualrois/.git

Afterwards, a test retrieval of some files with ``datalad get`` confirmed success.
To propagate the location update to the central dataset on GitHub, the ``annex`` branch
needs to be pushed there.
A regular ``datalad push --to origin`` should suffice.
The output should indicate that the annex branch was updated::

    $ datalad push
    publish(ok): . (dataset) [refs/heads/git-annex->origin:refs/heads/git-annex 304f2250..3a9c6331]
    action summary:
       publish (notneeded: 1, ok: 1)

To ensure everything worked as intended, the updated dataset was cloned again to
test if data retrieval succeeded.


Alternatives
------------

In the future, git-annex may provide a dedicate management command for this purpose. See https://git-annex.branchable.com/bugs/Disabling_remote_auto-enabling_not_possible for updates.
