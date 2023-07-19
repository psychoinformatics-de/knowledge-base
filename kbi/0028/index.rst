.. index::
   single: <topic>; <subtopic>

KBI0028: Create a DataLad dataset from Nextcloud (Sciebo) public share links
============================================================================

:authors: Name <email>
:discussion: <link>
:keywords: comma-separated list, aids, discoverability
:software-versions: <name>_<version>, ... (datalad or other version(s) used when crafting the KBI)

A DataLad dataset can be created directly from an existing collection
of files in a cloud storage, using share URLs to provide file
access. Nextcloud, and Nextcloud-based regional university service
Sciebo, are examples of cloud storage which allows generation of
folder share URLs with optional password protection. These can be use
to share data with managed permissions (password or named user), where
DataLad access is optional.

This document extends :ref:`KBI0007` in two areas: it introduces the
uncurl special remote for URL rewriting and credentials access, and
focuses on Nextcloud-specific URL patterns.

This document deals specifically with files that were deposited in
Nextcloud without using DataLad. For publishing DataLad datasets to
Nextcloud, see documentation of the create sibbling webdav command.

Nextcloud URL patterns
----------------------

There are three primary ways in which a Nextcloud folder can be shared. These will determine the URL patterns which can be used.

Public share link, no password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the sharing link is password protected, the URL above would not work, as it would redirect requests to a login page. In this case, as well as for sharing with named users only, WebDAV access can be used instead.

Named user share
^^^^^^^^^^^^^^^^

If a folder is shared with a named user, they will see it in their own account like any other folder, so in principle their access and owner access would be the same, and use an URL starting with:

.. code-block:: none

   https://example.com/nextcloud/remote.php/dav/files/USERNAME/

However, with Nextcloud (Sciebo) being a federated service, each user
may have a different instance URL to access their data. Additionally,
the URL includes the username, and each user may place the shared
directory in a different place within their home directory.

Public share, password protected
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For a folder shared with a password-protected link, the access URLs would start with:

.. code-block:: none

   https://example.com/nextcloud/public.php/webdav

The share token needs to be provided as username, and the (optional) share password as password -- as request credentials, not part of the URL.

URL pattern - summary
^^^^^^^^^^^^^^^^^^^^^

For the WebDAV url, it is useful to represent the share URL as the list of the following components:

.. code-block:: none

   https://<instance>/<accesspath>/<basepath>/<relpath>

where:

* ``<instance`` is the instance URL
* ``<accesspath>`` is either ``remote.php/dav/files/USERNAME/`` or
  ``public.php/webdav``
* ``<basepath>`` is the path to the shared folder in a given user's
  home directory (none for public shares)
* ``<relpath>`` is the path to a particular file relative to the
  shared folder (``<basepath>``)

Listing files
-------------

For generating the dataset, a list of file names (relative paths) and
their respective URLs is needed. These can be generated automatically, e.g. with the webdav4 and fsspec Python libraries.

An example script is given below, using inline comments for explanations.

The example assumes that user's webdav credentials are already known to DataLad under the name ``sciebo`` (if not, these can be added with ``datalad credentials add``, or provided to the script in a different way).

.. literalinclude:: list_files.py
   :language: python

