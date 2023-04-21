.. index::
   triple: git-annex; uninit; remove dataset annex

KBI0008: Remove a dataset's annex
=================================

:authors: Christian Mönch <christian.moench@web.de>
:discussion: https://github.com/datalad-handbook/book/issues/939
:keywords: annex, remove annex, annex uninit

This knowledge base item describes how to remove the annex from a DataLad
dataset and propagate that change to siblings

DataLad version used: this knowledge base item was created based on DataLad version 0.18.3


The scenario
------------

You have a DataLad dataset that has annexed files and you decide that you
don't want to use git-annex anymore in this dataset. This change should
also be propagated to all siblings of the dataset.


A few words of caution
......................

1. You should not remove the annex if you have large files, i.e. 1GB or larger, in your dataset. ``git`` is not intended for large files, which is the reason for the creation of ``git annex`` in the first place.

2. If you remove the annex, your files will be untracked in your dataset directory. That means, they are not versioned at this moment. If you don't follow the instructions in this knowledge base item precisely you might lose those files. Please be careful when you remove the annex! Work on a copy, or make sure that you have a sibling that contains your data. We do not want you to lose data.


Removing the annex
------------------

Go to the dataset from which you want to remove the annex and save the current state. Fetch all annexed data

.. code-block:: console

    > cd my_dataset
    > datalad save

Fetch all annexed data. Data that is not locally present when you remove the annex will not be locally present after removal of the annex.

.. code-block:: console

   > datalad get .


Now it is time to remove the annex. The command ``git annex uninit`` (`uninit documentation <https://git-annex.branchable.com/git-annex-uninit/>`_) will perform this task. 
But it will leave the now un-annexed files as "untracked" in the dataset:

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


If you want to keep their content, you **have** to make sure to add them to ``git`` before doing anything else. 
This can be done with a single ``git add .`` command in the root of the dataset if your dataset does not contain aditional untracked files that should not become part of the dataset content (if your dataset is not clean, you can add all files that you want to keep individually with the command ``git add <file-name>``). 
Afterwards you should execute a ``datalad save``. 
So the full sequence of commands are:

.. code-block:: console

    > git annex uninit
    > git add .
    > datalad save

That is it, no more annex files in your local dataset copy. If you want to push this dataset to siblings, read on.


Pushing an un-annexed dataset to a sibling
------------------------------------------

If your dataset has sibling datasets that were created and pushed to before running ``git annex uninit``, these siblings will still have an annex.
If you were to ``datalad push`` to or ``datalad update`` from these siblings, it would re-instate the git-annex branch in your dataset.
While this would not annex the previously annexed files again, it could cause future files to get annexed.
To prevent this, you have to delete the ``git-annex``-branch in the sibling before pushing or pulling updates.
Afterwards you can push the un-initialized dataset to the sibling. All subsequent clones from the sibling will have no annexed data. The following two commands will delete the ``git-annex``-branch from the sibling and push the un-initialized dataset to the sibling (we assume that the siblings name is ``a_sibling``):

.. code-block:: console

    > git push a_sibling ":git-annex"
    > datalad push -f gitpush --to a_sibling


That is it. Your sibling will have no more annex either.


A final warning
---------------

Do not remove the annex of a dataset that is shared with other users. Those users might not be able to ``datalad get`` data, and push- and update-operations might behave very unexpectedly and lead to data loss.

