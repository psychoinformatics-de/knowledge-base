.. index:: datalad; annex, git-annex,
.. highlight:: text

KBI0004: Why do files move to .git/annex/objects when converting an existing directory into a DataLad dataset?
==============================================================================================================

:authors: Stephan Heunis <jsheunis@gmail.com>, Christian Mönch <christian.moench@web.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/9
:keywords: datalad faq, git-annex faq, .git/annex/object, symlink, link

This knowledge-base item explains why files are moved into ``.git/annex/objects``, when
a DataLad dataset is created from an existing directory, or when a dataset with new files
is saved.


Question:
---------

On my Mac or Linux machine, when I convert an existing folder to a DataLad dataset, all files are moved to ``./.git/annex/objects/`` and
the file at the original location becomes a link to the moved content in ``./.git/annex/objects``. Is this
normal?


Answer:
-------

Yes, this is normal. DataLad manages your data with two main tools: ``git`` and ``git-annex``. The moving and linking is
used by ``git-annex`` to enable ``git`` to work well with very large files. By applying moving and linking, ``git-annex``
ensures that ``git`` only needs to track the links, which are quite small in size. The task of transporting and handling
the data content is performed by ``git-annex``.

This setup creates a modular and portable dataset (the ``git`` repository) which contains information about the versions
and history of data inside the dataset, while the actual data content is managed by ``git-annex``. File content that is
placed under management of ``git-annex`` will be moved into ``./.git/annex/objects/`` and a symbolic link (symlink) to
the content will remain in the original path. This symbolic link will be tracked by ``git``.

The separation of version management (done by ``git``) and content management (done by ``git-annex``)) make a DataLad
dataset very flexibld. You can for example share the dataset (``git`` repository) publicly, while keeping the contents
safe elsewhere. People can then access the dataset (with ``datalad clone``) and download individual files in the
dataset (with ``datalad get``) if they have access credentials for that particular storage location.

However, you can use configurations to specify how DataLad should commit/manage your data. You might want to commit all
your files to ``git`` (unless they are large, too numerous, or unless you don't want to make them available to
everybody who clones the ``git`` repository). You could also let every file be managed by ``git-annex``. Usually only
large binary files will be managed by ``git-annex`` by default.

The DataLad Handbook has very useful information on applying standard or custom configurations to your datasets:

* `5.1. DIY configurations — The DataLad Handbook 1 <https://handbook.datalad.org/en/latest/basics/101-122-config.html>`_
* `5.2. More on DIY configurations — The DataLad Handbook <https://handbook.datalad.org/en/latest/basics/101-123-config2.html>`_
* `5.3. Configurations to go — The DataLad Handbook <https://handbook.datalad.org/en/latest/basics/101-124-procedures.html>`_
