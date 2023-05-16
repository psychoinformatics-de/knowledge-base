.. index::
   single: <topic>; <subtopic>

KBI0015: Combining GitHub-like repositories and RIA stores
==========================================================

:authors: Michał Szczepanik <m.szczepanik@fz-juelich.de>
:discussion: <link>
:keywords: comma-separated list, aids, discoverability
:software-versions: <name>_<version>, ... (datalad or other version(s) used when crafting the KBI)

RIA stores are a convenient way of storing DataLad datasets on
computing architecture: personal computers, servers or compute
clusters.

Users may combine a RIA store with a GitHub-like repository that
serves as a "front-end" (entry point, or a place for collaboration
with pull-requests).

This document describes how to configure a subdataset so that clones
made from GitHub-like repositories can access subdatasets from RIA
stores.

While it targets primarily nested datasets, parts of the KBI also
apply to single datasets.

Subdataset source candidates
----------------------------

In a superdataset

::
   
   git config -f .datalad/config datalad.get.subdataset-source-candidate-000mypreferredRIAstore ria+http://store.datalad.org#{id}


Manual reconfiguration
----------------------

::
   
   datalad configuration get annex.uuid
   git remote add
   datalad foreach-dataset ...

Note: plans to allow autoenabling other than origin

Reconfigure
-----------

::
   
   datalad create-sibling-ria --existing reconfigure

Sources
-------

* http://handbook.datalad.org/en/latest/beyond_basics/101-147-riastores.html
* https://handbook.datalad.org/en/stable/beyond_basics/101-148-clonepriority.html
* https://handbook.datalad.org/en/stable/basics/101-123-config2.html#datalad-config
* https://github.com/datalad/datalad-next/issues/170
