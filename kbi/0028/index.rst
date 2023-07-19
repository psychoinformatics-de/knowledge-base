.. index::
   single: datalad; addurls
   single: special remote; uncurl

KBI0028: Create a DataLad dataset from Nextcloud (Sciebo) public share links
============================================================================

:authors: Michał Szczepanik <m.szczepanik@fz-juelich.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/104
:keywords: nextcloud, sciebo, webdav, sharing, addurls
:software-versions: datalad_0.19.2, datalad-next_1.0.0b3, webdav4_0.9.8, fsspec_2023.6.0, sciebo_10.12.2

A DataLad dataset can be created directly from an existing collection
of files in a cloud storage, using share URLs to provide file
access. `Nextcloud`_ storage platform (and, by extension, `Sciebo`_, a
Nextcloud-based regional university service) allows generation of
folder share URLs with optional password protection and expiration
time. Creating such share links, as well as granting access to
specific Nextcloud users, is an option for sharing data with managed
permissions. In such use case, DataLad is an optional method of
accessing and indexing data.

This document deals specifically with files that were deposited in
Nextcloud without using DataLad. For publishing DataLad datasets to
Nextcloud, see the documentation of DataLad-next's
`create-sibling-webdav`_ command instead.

This document extends :ref:`KBI0007` in two areas: it introduces the
`uncurl`_ special remote for transforming URLs and using credentials,
and focuses on Nextcloud-specific URL patterns.

.. _nextcloud: https://nextcloud.com/
.. _sciebo: https://hochschulcloud.nrw/
.. _create-sibling-webdav: https://docs.datalad.org/projects/next/en/latest/generated/man/datalad-create-sibling-webdav.html
.. _uncurl: https://docs.datalad.org/projects/next/en/latest/generated/datalad_next.annexremotes.uncurl.html#module-datalad_next.annexremotes.uncurl

Nextcloud URL patterns
----------------------

There are three primary ways in which a Nextcloud folder can be
shared. These will determine the URL patterns which can be used.

Public share link, no password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In a special (and simplest) case, if the sharing link for a folder is
created without password protection, links to individual files can be
created by appending ``/download?path=<path>&files=<name>`` (where
``path`` is a relative path to a directory, and ``name`` is the file
name). However, if the sharing link is password protected, such URL
would not work, as it would redirect to a login page (html document)
and not to file content.

In a general case (share links with or without password, as well as
sharing with named users), `Nextcloud's webdav access`_ can be
used. The remainder of the document only covers WebDAV URLs.

.. _nextcloud's webdav access: https://docs.nextcloud.com/server/20/user_manual/en/files/access_webdav.html

Named user share
^^^^^^^^^^^^^^^^

If a folder is shared with a named user, they will see it in their own
account like any other folder. In principle, access for a share
recipient would be analogous to that of an owner, and use an URL
starting with:

.. code-block:: none

   https://example.com/nextcloud/remote.php/dav/files/USERNAME/

However, with Nextcloud (Sciebo) being a federated service, each user
may have a different instance URL to access their data. Additionally,
the URL includes the username, and each user may place the shared
directory in a different place within their home directory.

Public share, password protected
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For a folder shared with a password-protected link, the access URLs
would start with:

.. code-block:: none

   https://example.com/nextcloud/public.php/webdav

The share token (part of the share link) needs to be provided as
username, and the (optional) share password as password. Note that
these are sent as request credentials, and are not included in the
URL.

URL pattern - summary
^^^^^^^^^^^^^^^^^^^^^

In summary, it is useful to represent the WebDAV URL as a combination
of the following components:

.. code-block:: none

   <instance>/<accesspath>/<dirpath>/<filepath>

where:

* ``<instance>`` is the instance URL
  (``https://example.com/nextcloud/`` in given examples)
* ``<accesspath>`` is either ``remote.php/dav/files/USERNAME/`` or
  ``public.php/webdav``
* ``<dirpath>`` is the path to the shared folder in user's home
  directory (none for public shares)
* ``<filepath>`` is the path to a particular file relative to the
  shared folder (``<dirpath>``)

Listing files
-------------

For generating the dataset, a list of file names (relative paths) and
their respective URLs is needed. These can be generated automatically,
e.g. with the `webdav4`_ and `fsspec`_ Python libraries.

An example script is given below, using inline comments for explanations.

The example assumes that user's webdav credentials are already known
to DataLad under the name ``webdav-mycred`` (if not, these can be
added with ``datalad credentials add``, or provided to the script in a
different way).

.. _webdav4: https://pypi.org/project/webdav4/
.. _fsspec: https://pypi.org/project/fsspec/

.. literalinclude:: list_files.py
   :language: python

This would produce the following csv file:

.. code-block:: none

   name,href
   file1.dat,/remote.php/dav/files/USERNAME/sharing/example/file1.dat
   foo/file2.dat,/remote.php/dav/files/USERNAME/sharing/example/foo/file2.dat
   ...
	      
Uncurl remote
-------------

Download URLs are handled by special remotes. The uncurl remote,
available in DataLad-next extension, provides both the ability to
reconfigure URLs and access to DataLad-next's credential workflow. It
can be initialized as follows (optionally with ``autoenable=true``):

.. code-block:: none

   git annex initremote uncurl type=external externaltype=uncurl encryption=none

With a known URL pattern (see above), a match expression can be
defined upfront. The regular expression below is relatively generic,
with only the dirpath being specific to the given example. Websites
like `regex101`_ can be helpful in building and understanding the
expression:

.. code-block:: none

   git annex enableremote uncurl match="(?P<instance>https://[^/]+)/(?P<accesspath>remote\.php/dav/files/[^/]+|public\.php/webdav)/(?P<dirpath>sharing/example)/(?P<filepath>.*)"

The dataset is created based on the previously generated tabular file
with ``datalad addurls``:

.. code-block:: none

   datalad addurls listing.txt https://example.com/nextcloud{href} {name}

.. _regex101: https://regex101.com

Transforming URLs
-----------------

Assuming the same user moves the folder in their Nextcloud account to
``some/other/place/``, the URL configuration can use all the defined
parts with only ``dirpath`` being different:

.. code-block:: none

   git annex enableremote uncurl url='{instance}/{accesspath}/some/other/place/{filepath}

A different user with whom the dataset is shared would have to
additionally replace ``accesspath``, and (possibly) ``instance``.

A user with whom the access was shared via a link would need to change
``accesspath``, and would not be using ``dirpath``:

.. code-block:: none

   git annex enableremote uncurl url='{instance}/public.php/webdav/{filepath}

Credential caveats
------------------

Regardless of whether the files are accessed via the
``remote.php/dav/files/USERNAME/`` or ``public.php/webdav`` path, the
authentication realm for the given nextcloud instance is the
same. This means users who already have DataLad credentials saved for
the given realm would be see their requests for password-protected
links refused. As long as ``get`` does not support explicit
credentials, this can be worked around by unsetting the credential
realm.

If a share link is not password protected, the webdav access via
``public.php/webdav`` can still be used. However, this requires
creating a DataLad credential with the token as username, and a
nonempty password (e.g. a single space or ``xyz``) that would not be used.
