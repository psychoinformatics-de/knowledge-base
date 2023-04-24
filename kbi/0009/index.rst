.. index::
   single: clone; copy

.. highlight:: console

KBI0009: How to re-ingest file content in a dataset clone
=========================================================

:authors: Adina Wagner <adina.wagner@t-online.de>
:discussion: <link>
:keywords: file content; copy; re-ingest file content
:software-versions: datalad_0.18.3, git-annex_10.20221003


Typically, transfer of data in DataLad datasets works best when
relying on the transport mechanisms provided by DataLad:
To obtain a copy of files from a dataset at location A to a different
location B, one would clone the dataset from A to B and retrieve its contents.

This KBI, though, outlines a rather unusual different method:
If a dataset at location A contains lots of data, and given that a complete
**copy of the data already exists outside of a DataLad dataset in location B**,
a plain clone from the dataset in A to B can be used to re-ingest the data.
The result is identical to having cloned and retrieved data, but without
duplicating the data transfer and instead using the pre-existing copy of the data.


Example workflow
----------------

Let's set up a toy example dataset at location A::

    # on one system
    $ datalad create location-A
    create(ok): /tmp/location-A (dataset)

Let's put some files inside. In this toy example it is only a single small file,
but the principles behind this demonstration hold independent of number or size
of files::

    $ datalad run -d /tmp/location-A 'dd if=/dev/urandom bs=1M count=10 of={dspath}/big.dat'
    [INFO   ] == Command start (output follows) =====
    10+0 records in
    10+0 records out
    10485760 bytes (10 MB, 10 MiB) copied, 0.0360015 s, 291 MB/s
    [INFO   ] == Command exit (modification check follows) =====
    run(ok): /tmp/location-A (dataset) [dd if=/dev/urandom bs=1M count=10 of=/tm...]
    add(ok): big.dat (file)
    save(ok): . (dataset)

Next, create a clone on the target system::

    $ datalad clone location-A:/tmp/location-A location-B
    install(ok): /tmp/location-B (dataset)

The clone knows about the file and its identity, but has not yet retrieved its
file contents::

    $ cd location-B
    $ ls -l .
    lrwxrwxrwx 1 adina adina 130 Apr 21 12:51 big.dat -> .git/annex/objects/1G/4J/MD5E-s10485760--49c360327aabc60e0b75e9bff4bee060.dat/MD5E-s10485760--49c360327aabc60e0b75e9bff4bee060.dat

Pay attention what the current commit SHA is to later easily identify any data
changes::

   $ git log -1 --pretty=oneline | cat
   ba083bf39f87bc97c60d70b1ff0c69e41cbf28a2 [DATALAD RUNCMD] dd if=/dev/urandom bs=1M count=10 of=/ho...

We can now copy or move over the files from a pre-existing copy into the worktree of the dataset::

   $ cp --remove-destination /place/with/copy /tmp/location-B

``datalad status`` will detect a change, because this replaced the symlink provided by git-annex with the actual data file::

   $ datalad status
   modified: big.dat (symlink)

The only thing left to finish the ingestion is a ``datalad save``.
If everything works as expected, i.e. the data copied is actually the data that
is expected/tracked, no new commit will be created::

    $ datalad save
    add(ok): big.dat (file)
    action summary:
      add (ok: 1)
      save (notneeded: 1)
    $ datalad status
    nothing to save, working tree clean
    $ git log -1 --pretty=oneline | cat
    ba083bf39f87bc97c60d70b1ff0c69e41cbf28a2 [DATALAD RUNCMD] dd if=/dev/urandom bs=1M count=10 of=/ho...

If the commit Shasum differs from the previously seen Shasum now, though, the
data that has been ingested isn't identical to the data originally tracked, for
example due to accidental corruption.




