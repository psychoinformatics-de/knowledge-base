.. index::
   single: datalad; addurls

KBI0007: Create a DataLad dataset from a published collection of files
======================================================================

:authors: Michael Hanke <michael.hanke@gmail.com>
:discussion: <link>
:keywords: geo, eurostat, ftp, http

Sometimes data exists as (a collection of) individual files that can simply be
downloaded -- with or without requiring authentication. When such data needs to
be processed, or ingested into another system or database, it can make sense to
use a DataLad dataset as means to track the exact state of any downloaded data
and thereby define a precise starting point for further processing or
reporting. This is particularly relevant for data files that may change over
time.

This KBI describes a simple approach how any collection of files that are
accessible via some URL can be tracked in a DataLad dataset. This approach is
applicable to a large number of data sources, such as the `Eurostat`_ (the EU's
portal on statistics and data on Europe) that supports direct file access via
their `bulk download interface`_.

.. _Eurostat: https://ec.europa.eu/eurostat
.. _bulk download interface: https://ec.europa.eu/eurostat/data/bulkdownload


Solution
--------

As an example, we will generate a DataLad dataset for a data record in the
`Gene Expression Omnibus database`_ (GEO), where scientist from around the
world deposit various kinds of genetics data to facilitate reproducible science
and future research.

.. _Gene Expression Omnibus database: https://www.ncbi.nlm.nih.gov/geo

We want to create a dataset for the data available under accession number
GSE209630. GEO offers direct downloads to all four associated files via the
accession URL https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE209630.

Some of these files are compressed or archives. DataLad provides flexible means
to transform the original files into a format that is optimally suited for a
particular type of access or processing. However, here we keep it simple and
only want to track the files as they are and under the names given by GEO. In
order to achieve that, we put the filename (that could also specify leading
sub-directories within the dataset) and the associated access URL as two
columns in a small `CSV-formatted`_ text file, with one row for each file. The
resulting table is seen below, first rendered for readability, and afterwards
the exact same file is shown in its actual CSV text file format.

.. _CSV-formatted: https://en.wikipedia.org/wiki/Comma-separated_values

.. csv-table:: Content of GSE209630_files.csv
   :file: GSE209630_files.csv
   :encoding: utf-8
   :header-rows: 1

.. literalinclude:: GSE209630_files.csv

With this data-specific information ready, we can generate the DataLad dataset
in two steps automatically.

First we create a new dataset. This step can be skipped, if the files shall be added to an existing dataset.

.. code-block:: console

   % datalad create gse209630
   create(ok): /tmp/gse209630 (dataset)

We use the ``create`` command and the accession number for the name of the directory that shall contain the newly created DataLad dataset.

Next we can use the ``addurls`` command to populate the dataset with the files
given in the table. The command requires three parameters: 1) the path to the
CSV table; 2) the name of the table column with the access URL of a file; and
3) the name of the table column with the associated file name to be used in the
DataLad dataset.

.. code-block:: console

   % cd gse209630
   % datalad addurls ../GSE209630_files.csv {url} {filename}
   addurl(ok): /tmp/gse209630/GSE209630_family.soft.gz (file) [to GSE209630_family.soft.gz]                                                                
   addurl(ok): /tmp/gse209630/GSE209630_family.xml.tgz (file) [to GSE209630_family.xml.tgz]                                                                   
   addurl(ok): /tmp/gse209630/GSE209630_series_matrix.txt.gz (file) [to GSE209630_series_matrix.txt.gz]                                                       
   addurl(ok): /tmp/gse209630/GSE209630_RAW.tar (file) [to GSE209630_RAW.tar]                                                                                 
   metadata(ok): /tmp/gse209630/GSE209630_family.soft.gz (file)                                                                                               
   metadata(ok): /tmp/gse209630/GSE209630_family.xml.tgz (file)                                                                                               
   metadata(ok): /tmp/gse209630/GSE209630_series_matrix.txt.gz (file)                                                                                         
   metadata(ok): /tmp/gse209630/GSE209630_RAW.tar (file)                                                                                                      
   save(ok): . (dataset)                                                                                                                                      
   action summary:                                                                                                                                            
     addurl (ok: 4)
     metadata (ok: 4)
     save (ok: 1)

Upon completion, DataLad has downloaded all files, and registered both checksums and download URLs. The dataset is now ready to be used for any purpose.

.. code-block:: console

   % datalad status --annex
   4 annex'd files (34.7 MB recorded total size)
   nothing to save, working tree clean

Given that all files are hosted on GEO, there is no need to retain the downloaded copies. They can be dropped, and DataLad can be used to download them on-demand (via the ``get`` or the ``run`` commands).

.. code-block:: console

   % datalad drop .
   drop(ok): GSE209630_RAW.tar (file)
   drop(ok): GSE209630_family.soft.gz (file)
   drop(ok): GSE209630_family.xml.tgz (file)
   drop(ok): GSE209630_series_matrix.txt.gz (file)
   drop(ok): . (directory)
   action summary:
     drop (ok: 5)
   
   # check remaining size
   % du -sh .
   352K    .


The, now "hollow" DataLad dataset consumes minimal resources, and can be preserved as a provenance record, or it could be pushed to a service like GitLab or GitHub to promote further reuse.


Further reading
---------------

Here we looked at a simple collection of a small number of file that could also
be downloaded with a simple click in a browser window. However, the same approach can also scale to datasets comprising millions of files and terabytes of data. For more information on scalability, see the `Human Connectome Dataset use case`_ in the DataLad handbook.

.. _Human Connectome Dataset use case: https://handbook.datalad.org/r.html?HCP-dataset
