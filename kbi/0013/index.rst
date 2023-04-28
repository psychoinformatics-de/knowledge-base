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

Prepare a demo data source with two files (``file1.txt`` and ``file2.txt``). ::

    $ datalad create datasource
    create(ok): /tmp/datasource (dataset)
    $ echo 123 > datasource/file1.txt
    $ echo 456 > datasource/file2.txt
    $ datalad -C datasource save
    add(ok): file1.txt (file)
    add(ok): file2.txt (file)
    save(ok): . (dataset)
    action summary:
      add (ok: 2)
      save (ok: 1)

We will make a clone ``worksrc`` to copy the availability info *from*, and
create two target datasets (``target1`` and ``target2``) to copy the
availability info *to*::

    $ datalad clone datasource worksrc
    install(ok): /tmp/worksrc (dataset)

    $ datalad create target1
    create(ok): /tmp/target1 (dataset)

    $ datalad create target2
    create(ok): /tmp/target2 (dataset)

Export all availability info for ``file1.txt`` (excluding the location of the
working clone itself)::

    $ git -C worksrc annex filter-branch --exclude-repo-config-for=here --include-all-key-information --include-all-repo-config file1.txt
    1932768784ce2f6e3be74bd1993d8b4750680db5

Enrich the ``target1`` dataset (poor-man's implementation of what ``copy-file``
would do)::

    $ git -C target1 annex fromkey $(basename $(readlink worksrc/file1.txt)) file1.txt --force
    fromkey file1.txt ok
    (recording state in git...)

Fetch the ``git-annex`` export::

    $ git -C target1 fetch ../worksrc 1932768784ce2f6e3be74bd1993d8b4750680db5:copy-file-tmp/git-annex
    remote: Enumerating objects: 6, done.
    remote: Counting objects: 100% (6/6), done.
    remote: Compressing objects: 100% (5/5), done.
    remote: Total 6 (delta 0), reused 0 (delta 0), pack-reused 0
    Unpacking objects: 100% (6/6), 494 bytes | 494.00 KiB/s, done.
    From ../worksrc
     * [new ref]         1932768784ce2f6e3be74bd1993d8b4750680db5 -> copy-file-tmp/git-annex

Merge in::

    $ git -C target1 annex merge
    merge git-annex (merging copy-file-tmp/git-annex into git-annex...)
    (recording state in git...)
    ok

Now it is complete::

    $ git -C target1 annex whereis file1.txt
    whereis file1.txt (1 copy)
        9f565372-9ee3-4abc-b53f-28eb24abf6cf -- loj@jasper:/tmp/datasource
    ok

And as soon as location information is available, it is also actionable::

    $ git -C target1 remote add source /tmp/datasource
    $ git -C target1 annex get file1.txt
    get file1.txt (from source...)
    ok
    (recording state in git...)
    $ cat target1/file1.txt
    123

Now follow the same steps for ``file2.txt`` and ``target2``::

    $ git -C worksrc annex filter-branch --exclude-repo-config-for=here --include-all-key-information --include-all-repo-config file2.txt
    35d8f20962e6ce13d8fc77604a7c48ac0d2ec1da
    $ git -C target2 annex fromkey $(basename $(readlink worksrc/file2.txt)) file2.txt --force
    fromkey file2.txt ok
    (recording state in git...)
    $ git -C target2 fetch ../worksrc 35d8f20962e6ce13d8fc77604a7c48ac0d2ec1da:copy-file-tmp/git-annex
    remote: Enumerating objects: 6, done.
    remote: Counting objects: 100% (6/6), done.
    remote: Compressing objects: 100% (5/5), done.
    remote: Total 6 (delta 0), reused 0 (delta 0), pack-reused 0
    Unpacking objects: 100% (6/6), 492 bytes | 492.00 KiB/s, done.
    From ../worksrc
     * [new ref]         35d8f20962e6ce13d8fc77604a7c48ac0d2ec1da -> copy-file-tmp/git-annex
    $ git -C target2 annex merge
    merge git-annex (merging copy-file-tmp/git-annex into git-annex...)
    (recording state in git...)
    ok
    $ git -C target2 annex whereis file2.txt
    whereis file2.txt (1 copy)
        3a00326f-c97c-4b7e-bde9-4e812253c528 -- loj@jasper:/tmp/datasource
    ok
    $ git -C target2 remote add source /tmp/datasource
    $ git -C target2 annex get file2.txt
    get file2.txt (from source...)
    ok
    (recording state in git...)
    $ cat target2/file2.txt
    456

.. _datalad copy-file: http://docs.datalad.org/en/stable/generated/man/datalad-copy-file.html
