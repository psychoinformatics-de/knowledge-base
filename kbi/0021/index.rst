.. index::
   zenodo; publish dataset

KBI0021: Publishing a DataLad dataset to Zenodo
===============================================

:authors: Michał Szczepanik <m.szczepanik@fz-juelich.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/issues/24
:keywords: zenodo, special remote
:software-versions: datalad_0.18.3

This KBI discusses the currently available methods for publishing a
dataset to `Zenodo`_.

.. _zenodo: https://zenodo.org/

Partial solution 1: archive just the Git repository
---------------------------------------------------

An easy way to index a dataset in Zenodo is by publishing it to GitHub:

* publish the dataset to GitHub,
* test whether a clone made from GitHub is able to retrieve data (from other locations),
* log in to Zenodo and add the GitHub repository,
* create a release on GitHub to trigger DOI assignment on Zenodo.

`Detailed instructions`_ are available from the Canadian Open
Neuroscience Platform.

This method can be used to obtain a Zenodo record that corresponds to
a versioned dataset. However, as GitHub can only hold the Git part of
the dataset, no annexed files will be stored in Zenodo. Annexed file
contents will need to be published to a special remote elsewhere.

.. _`detailed instructions`: https://portal.conp.ca/share#datalad

Partial solution 2: upload files using an existing special remote implementation
--------------------------------------------------------------------------------

We are aware of one git-annex special remote implementation for
Zenodo, `git-annex-remote-zenodo`_. However, it is described as work
in progress, and in our testing it showed limited functionality (with
a small patch we were able to push files to Zenodo, and retrieve them
back, but only in one and same dataset -- not in a dataset clone).

See the discussion in the `DataLad Handbook repository issue #941`_
for a description of required steps (including changes to code).

.. _git-annex-remote-zenodo: https://github.com/alegrand/git-annex-remote-zenodo
.. _datalad handbook repository issue #941: https://github.com/datalad-handbook/book/issues/941
