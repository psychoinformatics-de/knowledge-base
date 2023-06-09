.. index::
   triple: git-annex; uninit; remove dataset annex

KBI0008: Remove a dataset's annex
=================================

:authors: Christian Mönch <christian.moench@web.de>
:discussion: https://github.com/datalad-handbook/book/issues/939
:keywords: annex, remove annex, annex uninit
:software-versions: datalad_0.18.3

This knowledge base item describes how to remove the annex from a DataLad
dataset and propagate that change to siblings


A few words of caution
......................

1. You should not remove an annex of a dataset, if you have large files (>100MB), or many files (>several MB) that are cumulatively large. ``git`` is not intended for large files, which is the reason for the creation of ``git annex`` in the first place.

2. Once you removed an annex, previously annexed files will then be untracked in the dataset's directory. That means, they are no longer versioned at that moment. If you do not follow these instructions precisely **you might lose the files' content**. It is safer to work on a dataset copy, or make sure that another dataset sibling still contains all files' content.


Removing the annex
------------------

Go to the dataset from which you want to remove the annex and save the current state.

.. code-block:: console

    > cd my_dataset
    > datalad save

Fetch all annexed data. File contents that are not locally present when the annex is removed can no longer be retrieved via ``datalad get``.

.. code-block:: console

   > datalad get .


Now it is time to remove the annex. The command ``git annex uninit`` (`uninit documentation <https://git-annex.branchable.com/git-annex-uninit/>`_) will perform this task. 
The command will leave the now un-annexed files as "untracked" in the dataset:

.. code-block:: console

    > git annex uninit
    unannex <your-file(s)> ok
    (recording state in git...)
    Deleted branch git-annex (was <SHA>).
    > git status
    Changes to be committed:
        (use "git restore --staged <file>..." to unstage)
            deleted:    <your-file>

     Untracked files:
        (use "git add <file>..." to include in what will be committed)
            <your-file>


Now you should execute a ``datalad save``, to re-add the unannexed files to the dataset. So the full sequence of commands are:

.. code-block:: console

    > git annex uninit
    > datalad save

That is it, no more annexed files in your local dataset copy.
If you want to push this dataset to siblings, read on.


Pushing an un-annexed dataset to a sibling
------------------------------------------

If your dataset has sibling datasets that were created and pushed to before running ``git annex uninit``, these siblings will still have an annex.
If you were to ``datalad push`` to or ``datalad update`` from these siblings, it would re-instate the git-annex branch in your dataset.
While this would not annex the previously annexed files again, it could cause future files to get annexed.
To prevent this, you have to delete the ``git-annex``-branch in the sibling before pushing or pulling updates.
Afterwards you can push the un-initialized dataset to the sibling. All subsequent clones from the sibling will
have no annexed data. The following two commands will delete the ``git-annex``-branch from the sibling and push
the un-initialized dataset to the sibling (we assume that the siblings name is ``a_sibling``):

.. code-block:: console

    > git push a_sibling ":git-annex"
    > datalad push -f gitpush --to a_sibling


That is it. Your sibling will have no more annex either.


Removing the annex from other clones of the dataset
---------------------------------------------------

Any previously existing clone of the newly un-annexed dataset will still contain annex-related data, even after a
``datalad update`` from an un-annexed sibling. As a result some data will be stored twice in the
dataset, once in the worktree and once in the directory ``.git/annex/objects``. In addition
the sibling will contain additional files in the directory ``.git/annex`` and a branch called ``git-annex``.
To remove both of these artefacts, execute the following commands from the root of your dataset:

.. code-block:: console

    > git annex uninit
    > rm -rf .git/annex/objects/*
    > git annex uninit



A final warning
---------------

Do not remove the annex of a dataset that is shared with other users. Those users might not be able to
``datalad get`` data, and push- and update-operations might behave very unexpectedly and lead to data loss.
