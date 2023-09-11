.. index::
   pair: dataverse; dataset

KBI0002: Represent a Dataverse dataset as a DataLad dataset
===========================================================

:authors: Michael Hanke <michael.hanke@gmail.com>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/9
:keywords: addurls, datalad-dataverse

The `Dataverse extension package`_ equips DataLad with the ability to deposit DataLad datasets
on Dataverse_ and later retrieve such DataLad datasets from Dataverse again.
However, if a non-DataLad dataset has been deposited on Dataverse already, there is no
convenient command provided that can generate a DataLad dataset from such a
deposit automatically. At the same time, it can be useful to nevertheless
have such a DataLad dataset, for example, to be able to declare a (versioned)
data dependency for using DataLad's built-in provenance tracking features.


Requirements
------------

The solution described here requires DataLad (tested with v0.18), and the
`Dataverse extension package`_ (tested with v1.0). In principle, this can also
be done with the `pyDataverse package`_ directly, but this has not been tested.


Solution
--------

The starting point is a DataLad dataset. It either already exists, or is created
with DataLad's ``create`` command::

    $ datalad create <path>

A new state of this dataset is populated to match the latest state of a Dataverse
dataset using the ``addurls-dataverse.py`` script that is shown below. it must be
executed with a Python environment that has the aforementioned software dependencies
installed. The scripts assumes to run in the root directory of the DataLad dataset
that shall be populated. The script requires a Dataverse API token to be set via
the ``DATAVERSE_API_TOKEN`` environment variable. This token can be obtained from
the Dataverse web UI (see the `Dataverse extension package`_ documentation for
details). Moreover, the script requires two positional arguments:

1. the base URL of the Dataverse instance that is hosting the dataset
2. the persistent identifier (PID) of the Dataverse dataset to be queried

The PID can be found in the "Metadata" tab of the dataset's page on Dataverse.

An example script call looks like::

   # needs to be using the `set` command on Windows
   $ export DATAVERSE_API_TOKEN=99ad0817-....-....-....-279a39346c70
   $ python <path-to-script> 'https://dataverse.example.com' 'doi:10.26165/...'

When executed, the script will output progress information on files being
processed. No data will be downloaded. The local DataLad dataset is populated with
information from the metadata query alone.

Once finished, the DataLad dataset will show (untracked) changes. Those need to be
saved::

   $ datalad save ...

It is recommended to include an appropriate commit message.

Afterwards the DataLad dataset is ready for (re-)use and supports standard DataLad
operations like ``get``, and can be added as a subdataset to other datasets. Please
note that the generated DataLad dataset needs to be hosted somewhere in order to be
accessible. However, there is no requirement to host a copy of the data files stored
on Dataverse.

Limitations
-----------

The script shown here assumes:

1. the targeted Dataverse instance is reporting SHA256 checksums. If that is
   not the case, and, for example MD5SUMs are reported. The script needs to be
   adjusted accordingly.
2. the queried Dataverse dataset must be public (file access permitted without
   particular permissions). The presented solution could be extended to access-protected
   dataset, but this has not been explored.

.. _Dataverse extension package: https://github.com/datalad/datalad-dataverse
.. _Dataverse: https://dataverse.org
.. _pyDataverse package: https://github.com/gdcc/pyDataverse


.. literalinclude:: addurls-dataverse.py
   :language: python
   :linenos:
   :caption: addurls-dataverse.py
