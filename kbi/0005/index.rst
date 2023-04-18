.. index:: datalad; drop, subdataset

KBI0005: Drop a subdataset to speed up superdataset operations
==============================================================

:authors: Laura Waite <laura@waite.eu>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/21
:keywords: subdataset, datalad drop

In certain situations, superdatasets can contain heavy subdatasets (e.g. with
many files) that slow down dataset operations.

A common example of this is a BIDS dataset with a nested ``sourcedata``
subdataset that contains the source DICOM files from the file format conversion
to NIfTI.

::

   bids_ds
   ├── sourcedata
   │   └── DICOM
   │       └── data1.dcm -> ../../.git/annex/objects/WF/m1/MD5E-s8--2eade17812e56a0028cb69f7813fc33c.dcm/MD5E-s8--2eade17812e56a0028cb69f7813fc33c.dcm
   │       └── data2.dcm -> ../../.git/annex/objects/WF/m1/MD5E-s8--2eade17812e56a0028cb69f7813fc33c.dcm/MD5E-s8--2eade17812e56a0028cb69f7813fc33c.dcm
   │       └── data3.dcm -> ../../.git/annex/objects/WF/m1/MD5E-s8--2eade17812e56a0028cb69f7813fc33c.dcm/MD5E-s8--2eade17812e56a0028cb69f7813fc33c.dcm
   ├── sub-01
   ├── sub-02
   └── sub-03


Solutions
---------

Drop the subdatatset
********************

If the sourcedata does not need to be kept locally (and it already lives in
another secure location), the simplest solution is to drop the subdataset::

$ cd bids_ds
$ datalad drop -d . --what datasets sourcedata

If the sourcedata does not live in another secure location (meaning the file
content can't safely be dropped), see the `DataLad Handbook`_ for examples of
how to configure siblings to be able to push the data to a new location.

.. _DataLad Handbook: http://handbook.datalad.org/en/latest/basics/101-141-push.html#the-general-overview
