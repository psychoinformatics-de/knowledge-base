.. _0024:

.. index::
   single: RIA; archive
.. highlight:: console

KBI0024: Create and update a 7-Zip archive in a RIA store
=========================================================

:authors: Laura Waite <laura@waite.eu>, Michael Hanke <michael.hanke@gmail.com>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/issues/47
:keywords: RIA, archive, 7-Zip, inodes
:software-versions: datalad_0.18.3

When working with `RIA stores`_, it is possible to compress the
``annex/objects`` into `7-zip`_ archives. With this approach, the entire
annex object store can be put into an archive and remain fully accessible while
minimizing `inodes`_, regardless of file number and size. This is beneficial
for compression gains or when operating on HPC-systems with inode limitations.

This document describes how to create a 7-Zip archive for an existing RIA
store using the script shown below. The script does the following:

1. Remove non-essential files and directories within the RIA store (e.g. hooks,
   etc). This aspect has nothing to do with creating the archive, but is useful
   for reducing the number of inodes.
2. Create a 7-Zip archive containing the content in the annex object store.
3. Clean-up (remove) the content in the annex object store after it is
   archived.

The script can also be used to update an archive if it already exists, as it
uses the update flag when calling 7-Zip (``7z u``).

Preparation
-----------

Populate a DataLad dataset::

  $ datalad create my_dataset
  $ cd my_dataset
  $ echo "file 1 content" > file1.txt
  $ datalad save -m "add file1 to the dataset"

Create a RIA store::

  $ datalad create-sibling-ria -d ./ -s ria-store --new-store-ok "ria+file:///tmp/my_store"
  $ datalad push --to ria-store
  $ cd ../

Create an archive
-----------------

First take a look at the state of the RIA store. Content exists under
``annex/objects``::

  $ tree my_store
  my_store
  ├── 1e9
  │   └── 91f14-baff-4565-8b38-fceed63bb805
  │       ├── annex
  │       │   └── objects
  │       │       └── v2
  │       │           └── 2W
  │       │               └── MD5E-s15--af1cdf0b10caa12cf13312f7bb4215df.txt
  │       │                   └── MD5E-s15--af1cdf0b10caa12cf13312f7bb4215df.txt
  │       ├── archives
  │       ├── branches
  │       ├── config
  │       ├── config.dataladlock
  │       ├── description
  │       ├── HEAD
  │       ├── hooks
  │       │   ├── applypatch-msg.sample
  │       │   ├── commit-msg.sample
  │       │   ├── fsmonitor-watchman.sample
  │       │   ├── post-update.sample
  │       │   ├── pre-applypatch.sample
  │       │   ├── pre-commit.sample
  │       │   ├── pre-merge-commit.sample
  │       │   ├── prepare-commit-msg.sample
  │       │   ├── pre-push.sample
  │       │   ├── pre-rebase.sample
  │       │   ├── pre-receive.sample
  │       │   ├── push-to-checkout.sample
  │       │   └── update.sample
  │       ├── info
  │       │   └── exclude
  │       ├── objects
  │       │   ├── 08
  │       │   │   └── e3ea145c77abd0cf9cb07f04f069efed2bd637
  │       │   ├── 0d
  │       │   │   └── 81baa2295544cae79101a18f6473a6c917b927
  │       │   ├── [...]
  │       │   │   └── [...]
  │       │   ├── info
  │       │   └── pack
  │       ├── ora-remote-e9bef249-aeea-46b6-b9f3-f8e0c10c1931
  │       │   └── transfer
  │       ├── refs
  │       │   ├── heads
  │       │   │   ├── git-annex
  │       │   │   └── master
  │       │   └── tags
  │       └── ria-layout-version
  ├── error_logs
  └── ria-layout-version


Create the archive using the ``cleanup.sh`` script shown below::

  $ find my_store -mindepth 2 -maxdepth 2 -type d | xargs -n1 bash cleanup.sh

As a result, the store should look like this::

  $ tree my_store
  my_store
  ├── 1e9
  │   └── 91f14-baff-4565-8b38-fceed63bb805
  │       ├── archives
  │       │   └── archive.7z
  │       ├── branches
  │       ├── config
  │       ├── config.dataladlock
  │       ├── description
  │       ├── HEAD
  │       ├── objects
  │       │   ├── 08
  │       │   │   └── e3ea145c77abd0cf9cb07f04f069efed2bd637
  │       │   ├── 0d
  │       │   │   └── 81baa2295544cae79101a18f6473a6c917b927
  │       │   ├── [...]
  │       │   │   └── [...]
  │       │   ├── info
  │       │   └── pack
  │       ├── refs
  │       │   ├── heads
  │       │   │   ├── git-annex
  │       │   │   └── master
  │       │   └── tags
  │       └── ria-layout-version
  ├── error_logs
  └── ria-layout-version


Update an archive
-----------------

The same script (``cleanup.sh``) can be used to update an already existing
archive within a RIA store.

Make a fresh clone from the RIA store::

  $ datalad clone "ria+file:///tmp/my_store#1e991f14-baff-4565-8b38-fceed63bb805" my_clone
  $ cd my_clone

Add another file to the dataset::

  $ echo "file 2 content" > file2.txt
  $ datalad save -m "add file2 to the dataset"
  $ datalad push --to origin
  $ cd ../

Take look at the state of the store. Since we added a new file, there is again
content under ``annex/objects``::

  $ tree my_store
  my_store
  ├── 1e9
  │   └── 91f14-baff-4565-8b38-fceed63bb805
  │       ├── annex
  │       │   └── objects
  │       │       └── Pf
  │       │           └── vq
  │       │               └── MD5E-s15--7a593f3460f1efc629489d5a9e86c7b0.txt
  │       │                   └── MD5E-s15--7a593f3460f1efc629489d5a9e86c7b0.txt
  │       ├── archives
  │       │   └── archive.7z
  │       ├── branches
  │       ├── config
  │       ├── config.dataladlock
  │       ├── description
  │       ├── HEAD
  │       ├── objects
  │       │   ├── 08
  │       │   │   └── e3ea145c77abd0cf9cb07f04f069efed2bd637
  │       │   ├── 0d
  │       │   │   └── 81baa2295544cae79101a18f6473a6c917b927
  │       │   ├── [...]
  │       │   │   └── [...]
  │       │   ├── info
  │       │   └── pack
  │       ├── ora-remote-5a413a03-91cb-4433-a2b5-e2d108ec291b
  │       │   └── transfer
  │       ├── refs
  │       │   ├── heads
  │       │   │   ├── git-annex
  │       │   │   └── master
  │       │   └── tags
  │       └── ria-layout-version
  ├── error_logs
  └── ria-layout-version


Run the ``cleanup.sh`` script again to update the archive with the new objects::

  $ find my_store -mindepth 2 -maxdepth 2 -type d | xargs -n1 bash cleanup.sh
  $ tree my_store
  my_store
  ├── 1e9
  │   └── 91f14-baff-4565-8b38-fceed63bb805
  │       ├── archives
  │       │   └── archive.7z
  │       ├── branches
  │       ├── config
  │       ├── config.dataladlock
  │       ├── description
  │       ├── HEAD
  │       ├── objects
  │       │   ├── 08
  │       │   │   └── e3ea145c77abd0cf9cb07f04f069efed2bd637
  │       │   ├── 0d
  │       │   │   └── 81baa2295544cae79101a18f6473a6c917b927
  │       │   ├── [...]
  │       │   │   └── [...]
  │       │   ├── info
  │       │   └── pack
  │       ├── refs
  │       │   ├── heads
  │       │   │   ├── git-annex
  │       │   │   └── master
  │       │   └── tags
  │       └── ria-layout-version
  ├── error_logs
  └── ria-layout-version


Let's verify that the archive was updated successfully with the new content,
using the dataset we started with::

  $ cd my_dataset

This dataset only has one file (``file1.txt``)::

  $ tree
  .
  └── file1.txt -> .git/annex/objects/v2/2W/MD5E-s15--af1cdf0b10caa12cf13312f7bb4215df.txt/MD5E-s15--af1cdf0b10caa12cf13312f7bb4215df.txt


Run ``datalad update`` to bring in the updates from the RIA store (i.e. ``file2.txt``)::

  $ datalad update --merge
  $ tree
  .
  ├── file1.txt -> .git/annex/objects/v2/2W/MD5E-s15--af1cdf0b10caa12cf13312f7bb4215df.txt/MD5E-s15--af1cdf0b10caa12cf13312f7bb4215df.txt
  └── file2.txt -> .git/annex/objects/Pf/vq/MD5E-s15--7a593f3460f1efc629489d5a9e86c7b0.txt/MD5E-s15--7a593f3460f1efc629489d5a9e86c7b0.txt



.. literalinclude:: cleanup.sh
   :language: bash
   :linenos:
   :caption: cleanup.sh

.. _ria stores: http://handbook.datalad.org/en/latest/beyond_basics/101-147-riastores.html
.. _7-Zip: https://www.7-zip.org/
.. _inodes: https://en.wikipedia.org/wiki/Inode
