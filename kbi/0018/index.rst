.. index::
   configuration; subdataset source candidate
   RIA; with other siblings
.. highlight:: console

KBI0018: Combining GitHub-like repositories and RIA stores
==========================================================

:authors: Michał Szczepanik <m.szczepanik@fz-juelich.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/73
:keywords: RIA, GitHub, configuration, clone, source candidate
:software-versions: datalad_0.18.3

`RIA stores`_ are a convenient way of storing DataLad datasets on
computing architecture: personal computers, servers or compute
clusters. Users may combine a RIA store with an outward-facing
GitHub-like repository (landing page, collaboration hub). In many such
configurations, only the top-level dataset would be pushed to GitHub,
while its subdatasets would be kept only in RIA.

This document describes how to configure a superdataset so that clones
made from GitHub-like repositories can access subdatasets from RIA
stores. We focus primarily on the
``datalad.get.subdataset-source-candidate`` setting.

Although the KBI targets nested datasets, some of the information also
applies to single datasets.

Subdataset source candidates
----------------------------

A subdataset source candidate can be configured in the superdataset::

   $ git config -f .datalad/config datalad.get.subdataset-source-candidate-000mypreferredRIAstore ria+ssh://path/to/store#{id}

The last part of the option name (``000mypreferredRIAstore``) combines
a three-digit *cost* and an arbitrary name of the candidate. Clone
candidates will be tried in the order of increasing cost. Note that
there are some default candidates, including the superdataset’s remote URL
with submodule path appended, and the submodule url stored in
``.gitmodules`` file (cost 500 and 600 respectively). See
`Prioritizing subdataset clone locations`_ chapter in the DataLad
Handbook for more information.

Writing the configuration option to ``.datalad/config`` (a
repository-specific file which is version controlled and shared with
the dataset) ensures that it will be available in dataset
clones. Naturally, the option can also be set in a dataset clone
afterwards, and placed e.g. in ``.git/config`` (a repository-specific
file which is not version controlled). See `More on DIY
configurations`_ chapter in the DataLad Handbook for more information
about configuration files.


Example
^^^^^^^

Assuming the following dataset structure (``datalad tree`` command is provided by `datalad-next`_ extension)::

  $ datalad tree
  [DS~0] /tmp/foo
  ├── [DS~1] bar/
  └── [DS~1] baz/

Configure and publish
"""""""""""""""""""""

We create the RIA store and siblings for all datasets, and an additional GitHub sibling for the superdaset only (without ``--recursive``)::

  $ datalad create-sibling-ria --recursive --new-store-ok --name ria-store "ria+ssh://example.com/path/to/store"
  $ datalad create-sibling-github --name github <repo-name>

We then set the RIA location as the top subdataset source candidate, and save this configuration file change in the dataset::

  $ git config -f .datalad/config datalad.get.subdataset-source-candidate-000-myPreferredRiaStore "ria+ssh://example.com/path/to/store#{id}"   
  $ datalad save -m "Added source candidate config" .datalad/config

We push all datasets to the RIA store, and the superdataset additionally to GitHub::

  $ datalad push --recursive --to ria-store
  $ datalad push --to github

Clone and get
"""""""""""""

Clone from GitHub into another location::

  $ cd ..
  $ datalad clone <github repo url> <clone target>
  $ cd <clone target>

The clone is able to install a subdataset - it does so from the preferred location::

  $ datalad get --no-data bar
  [INFO   ] Configure additional publication dependency on "ria-store-storage"                                                                  
  install(ok): /tmp/<repo-name>/bar (dataset) [Installed subdataset in order to get /tmp/<repo-name>/bar]

The subdataset's origin is the respective location in the RIA store; the ``*-storage`` special remote is enabled automatically::

  $ datalad siblings -d bar
  .: here(+) [git]
  .: origin(-) [ssh://example.com/path/to/store/7df/cc05d-b7ba-4b32-b7b0-9f9bb6edcf9d (git)]
  .: ria-store-storage(+) [ora]

The top level dataset also has its ``*-storage`` remote enabled automatically, but since it was cloned from GitHub, its origin remote points there::

  $ datalad siblings -d .
  .: here(+) [git]
  .: origin(-) [<github repo url> (git)]
  .: ria-store-storage(+) [ora]


Adding RIA git remote manually
------------------------------

The dataset which was cloned directly from GitHub (superdataset in the
example above) has GitHub as its origin. The ``ria-store-storage``
(autoenabled git-annex special remote) is already available, but the
git remote (formerly named ``ria-store``) is not. If we want to push
superdatsets's git updates (not just annexed contents) back to the RIA
store, we need to configure the git remote.

There are plans to `allow adding git remotes other than origin`_
automatically, but no implementation yet.

Although it was created as part of a RIA store, the git remote is no
different from any other git remote, and can be enabled with ``git
remote add``. We need to know the store URL, and dataset ID. Since
this is a git remote, we cannot use the ``ria+``, ``#{id}`` or
``#~alias`` notation, and we have to split the ID with a path
separator after the first three characters::

   $ datalad configuration get datalad.dataset.id
   4183e386-1fb7-467c-a508-cea7d6b1f8e6
   $ git remote add ria-store "ssh://example.com/path/to/store/418/3e386-1fb7-467c-a508-cea7d6b1f8e6"

If for some reason this step needs to be repeated for all subdatasets
(e.g. they were installed from another source) it should be possible
to create a short script that figures out the URL, and run it with
``datalad foreach-dataset``.

Gitmodules file
---------------

Since in our example the subdatasets were created using ``datalad
create`` (rather than cloned into the superdataset), their urls only
record the local path:

.. code-block:: cfg

  [submodule "bar"]
        path = bar
        url = ./bar
        datalad-id = 7dfcc05d-b7ba-4b32-b7b0-9f9bb6edcf9d

Had the superdataset been cloned from a ``ria+[http|https|ssh]`` URL,
no source candidate configuration would be necessary, as DataLad would
(by default) use the combination of superdataset origin and the local
path as one of the source candidates. This would naturally not work
when the superdataset is on GitHub, and subdatasets are not.

However, the gitmodules file can be edited to contain the "right" URL,
as it is also one of the default source candidates:

.. code-block:: cfg

  [submodule "bar"]
        path = bar
        url = ssh://example.com/path/to/store/7df/cc05d-b7ba-4b32-b7b0-9f9bb6edcf9d
        datalad-id = 7dfcc05d-b7ba-4b32-b7b0-9f9bb6edcf9d
        datalad-url = "ria+ssh://example.com/path/to/store#7dfcc05d-b7ba-4b32-b7b0-9f9bb6edcf9d"

Reconfigure
-----------

Finally, it is possible to recreate the git remote and special remote
configuration in a clone by repeating the ``create-sibling-ria``
command and asking it to reconfigure existing siblings::

   $ datalad create-sibling-ria --existing reconfigure ...

However, like any ``create-sibling-*`` command, ``create-sibling-ria``
performs configuration on local *and remote* end. In the current
example, it would connect to the ssh server and attempt re-running
initialization code. While in many cases it would only end up changing
local configuration, its lower performance and the risk of altering
existing remote configuration make this option less preferable than
the alternatives above.

.. _ria stores: http://handbook.datalad.org/en/latest/beyond_basics/101-147-riastores.html
.. _prioritizing subdataset clone locations: https://handbook.datalad.org/en/stable/beyond_basics/101-148-clonepriority.html
.. _more on DIY configurations: https://handbook.datalad.org/en/stable/basics/101-123-config2.html#datalad-config
.. _datalad-next: https://github.com/datalad/datalad-next
.. _allow adding git remotes other than origin: https://github.com/datalad/datalad-next/issues/170
