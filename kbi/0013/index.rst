.. index::
   single: filter-branch; merge; copy-file

.. highlight:: console

KBI0013: Split a dataset without touching hosted data
=====================================================

:authors: Laura Waite <laura@waite.eu>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/45
:keywords: git-annex-filter-branch, availability info
:software-versions: datalad_0.18.3, git-annex_10.20230126

Situations can arise when one wishes to split apart an existing large
dataset into multiple subdatasets. The command `datalad copy-file`_ works very
well for this when file ability information is URL-based; however, this is not
always the case. While there is not yet DataLad tooling to do this, there
is a workflow using ``git-annex-filter-branch`` that can achieve the desired
outcome.

It is important to note that this approach will not preserve prior history.

Example workflow
----------------

Prepare a demo data source::

    $ datalad create datasource                                                                                              130 !
    create(ok): /tmp/datasource (dataset)
    $ echo 123 > datasource/file1.txt
    $ datalad -C datasource save
    add(ok): file1.txt (file)
    save(ok): . (dataset)
    action summary:
      add (ok: 1)
      save (ok: 1)

In most cases, one would want to work with a clone of the data source. We will
make a clone ``worksrc`` to copy the availability info *from*, and create a
``target`` dataset to copy the availability info *to*::

    $ datalad clone datasource worksrc
    install(ok): /tmp/worksrc (dataset)

    $ datalad create target                                                                                                  128 !
    create(ok): /tmp/target (dataset)

Export all availability info for ``file1.txt`` (excluding the location of the
working clone itself)::

    $ git -C worksrc annex filter-branch --exclude-repo-config-for=here --include-all-key-information --include-all-repo-config file1.txt
    1932768784ce2f6e3be74bd1993d8b4750680db5

Enrich the ``target`` dataset (poor-man's implementation of what ``copy-file``
would do)::

    $ git -C target annex fromkey $(basename $(readlink worksrc/file1.txt)) file1.txt --force
    fromkey file1.txt ok
    (recording state in git...)

Fetch the ``git-annex`` export::

    $ git -C target fetch ../worksrc 1932768784ce2f6e3be74bd1993d8b4750680db5:copy-file-tmp/git-annex
    remote: Enumerating objects: 6, done.
    remote: Counting objects: 100% (6/6), done.
    remote: Compressing objects: 100% (5/5), done.
    remote: Total 6 (delta 0), reused 0 (delta 0), pack-reused 0
    Unpacking objects: 100% (6/6), 494 bytes | 494.00 KiB/s, done.
    From ../worksrc
     * [new ref]         1932768784ce2f6e3be74bd1993d8b4750680db5 -> copy-file-tmp/git-annex

Merge in::

    $ git -C target annex merge
    merge git-annex (merging copy-file-tmp/git-annex into git-annex...)
    (recording state in git...)
    ok

Now it is complete::

    $ git -C target annex whereis file1.txt
    whereis file1.txt (1 copy)
        9f565372-9ee3-4abc-b53f-28eb24abf6cf -- loj@jasper:/tmp/datasource
    ok

And as soon as location information is available, it is also actionable::

    $ git -C target remote add source /tmp/datasource
    $ get file1.txt (from source...)
    ok
    (recording state in git...)
    $ cat target/file1.txt
    123

.. _datalad copy-file: http://docs.datalad.org/en/stable/generated/man/datalad-copy-file.html