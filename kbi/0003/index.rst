.. index:: datalad; run, datalad; unlock
.. highlight:: text

KBI0003: Capturing interactive computations in Jupyter Notebooks
================================================================

:authors: Adina Wagner <a.wagner@fz-juelich.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/1
:keywords: datalad run, run, unlock

This knowledge-base item discusses how wrap interactive computing with
Jupyter Notebooks by invoking them from the terminal, wrapped in a
``datalad run`` call.

Overview
--------

Jupyter notebooks offer an interactive computing environment.
Just as any other files, they can be a part of a DataLad dataset, and
their code can use or modify files inside of DataLad datasets.

More so than computational scripts, they incentivize interactive
computations.
This bears at least two difficulties:

* modifying annexed files on the fly can cause permission errors
* keeping track of changes during interactive computing

Wrapping the entire execution of the notebook session into a
``datalad run`` command can alleviate those difficulties.
It can help to capture all changes in a session as long as the user
shuts down the Jupyter server orderly via the "Quit" button,
and it can unlock relevant files at the start if the user adds an
``--output`` specification to it.


Consider a dataset with an annexed file that will be modified in a
notebook session:

.. code-block:: bash

    ❱ datalad create mynotebookenv
    create(ok): /tmp/mynotebookenv (dataset)
    ❱ cd mynotebookenv
    ❱ echo 123456 > file
    ❱ datalad save -m "annexed something"
    add(ok): file (file)
    save(ok): . (dataset)
    action summary:
      add (ok: 1)
      save (ok: 1)

Wrapping a ``jupyter-notebook`` command (or a more specific
``jupyter-notebook <path-to-notebook>`` into ``datalad run`` with an
``--output`` declaration can capture any changes, and allows modifying
the annexed file:

.. code-block:: bash

    ❱ datalad run \
     -m "running jupyter notebook" \
     --output file "jupyter-notebook"
    unlock(ok): file (file)
    ...
    [Notebook logmessages]
    ...
    [INFO   ] == Command exit (modification check follows) =====
    run(ok): /tmp/mynotebookenv (dataset) [jupyter-notebook]
    add(ok): Untitled.ipynb (file)
    add(ok): file (file)
    save(ok): . (dataset)

This process will also work if the data to be unlocked or the Notebook
invoked are in different levels of a dataset hierarchy as long as the
paths to ``--input`` or ``--output`` declarations to not point upwards -
in other words, as long as the ``run`` command is executed from a same- or top-level dataset.

Here is an example with a subdataset that contains one annexed file:

.. code-block:: bash

   # create a dataset hierarchy, and some content
   ❱ datalad create super && \
   cd super && \
   datalad create -d sub && \
   echo 1234 > file && \
   datalad save -m "annex something"
   create(ok): /tmp/super (dataset)
   create(ok): . (dataset)
   add(ok): sub (dataset)
   add(ok): .gitmodules (file)
   add(ok): file (file)
   save(ok): . (dataset)
   action summary:
     add (ok: 3)
     save (ok: 1)

We can modify content in the subdataset as long as the command is run from the a dataset higher in the dataset hierarchy:

.. code-block:: bash

   ❱ datalad run \
   -m "running jupyter notebook to modify subdataset content" \
   --output sub/file \
   "jupyter-notebook Untitled.ipynb"
   unlock(ok): sub/file (file)
   [INFO   ] == Command start (output follows) =====

   [Notebook log output]

   [INFO   ] == Command exit (modification check follows) =====
   run(ok): /tmp/super (dataset) [jupyter-notebook Untitled.ipynb]
   add(ok): file (file)
   save(ok): sub (dataset)
   add(ok): sub (dataset)
   add(ok): .gitmodules (file)
   save(ok): . (dataset)

It would not work if the ``--output`` specification points outside of the dataset:

.. code-block:: bash

   ❱ datalad create super && \
   cd super && \
   datalad create -d sub && \
   echo 1234 > file && \
   datalad save -m "annex something"
    create(ok): /tmp/super (dataset)
    create(ok): . (dataset)
    add(ok): sub (dataset)
    add(ok): .gitmodules (file)
    add(ok): file (file)
    save(ok): . (dataset)
    action summary:
      add (ok: 3)
      save (ok: 1)
   ❱ tree
   .
   ├── file -> .git/annex/objects/kj/05/MD5E-s5--e7df7cd2ca07f4f1ab415d457a6e1c13/MD5E-s5--e7df7cd2ca07f4f1ab415d457a6e1c13
   └── sub

   ❱ cd sub
   ❱ datalad run \
    -m "running jupyter notebook from subdataset" \
    --output ../file \
    "jupyter-notebook"
   get(error): .. [path not associated with dataset Dataset(/tmp/super/sub)]
