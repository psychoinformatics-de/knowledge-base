.. index::
   single: shared repository; multi-user

KBI0025:  Saving changes in datasets owned by other users
=========================================================

:authors: Adina Wagner <adina.wagner@t-online.de>
:discussion: <link>
:keywords: sharedRepository, git config, multi-user
:software-versions: datalad_0.19.0, git_2.39.2

It is generally recommended to not share one and the same dataset or Git
repository when collaborating with others.
In the typical workflow for collaboration, each user has their own clone of the
respective dataset instead.
One of several reasons why sharing the same dataset is not ideal is that
Git lets the operating system decide which Unix file permissions are applied,
and typical `umask`_ configurations give write permissions only to the file
owner, which in turn creates permission errors when a user other than the
dataset owner saves a modification.

But if a dataset needs to be shared among several users, the following Git
configuration can help:

.. _umask: https://en.wikipedia.org/wiki/Umask

core.sharedRepository
---------------------

The Git configuration ``code.sharedRepository`` can, when set to ``group`` (or
``true``), make a repository or dataset shared between several users in the
same Unix user `group`_.
This allows more users than just the dataset owner to save modifications.
Other values (such as `all`, `world`, or `everybody`) make this possible for an
even wider range of users, and the configuration can even take octal numbers that
define a precise `umask`_.
To use them wisely, its good to have an understanding of file permissions.
The NIH has an `excellent overview`_.

Here is an example configuration in a new dataset:

.. code-block:: console

   $ datalad create my-shared-dataset
     create(ok): /tmp/my-shared-dataset (dataset)
   $ cd my-shared-dataset
   $ git config core.sharedRepository true

Afterwards, users on the same system can commit or save changes into the
dataset as long as they are members of the same group.
This is identical to creating the datasets as shared repositories (``datalad
create myds --shared=group``, but does not require re-creating or
re-initializing them.


.. _group: https://en.wikipedia.org/wiki/Group_identifier
.. _excellent overview: https://hpc.nih.gov/storage/permissions.html

