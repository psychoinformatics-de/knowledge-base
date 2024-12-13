.. index::
   single: keyring; backends

.. highlight:: console

KBI0023: Keyring configuration
==============================

:authors: Michał Szczepanik
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/89
:keywords: keyring, credentials
:software-versions: datalad_0.18.3, datalad-next_0.6.3

This KBI covers keyring configuration in the context of problems with
credential retrieval observed on a headless system. It also provides a
general overview of keyring access.

Problem description and troubleshooting
---------------------------------------

DataLad uses the `Keyring`_ Python library to communicate with keyring
backends available on the given system to store user's credentials.

.. _Keyring: https://keyring.readthedocs.io/

Keyring information, including the active backends and the location of
a keyring configuration file, can always be found in the output of
``datalad wtf``::

  $ datalad wtf --section credentials
  # WTF
  ## credentials
  - keyring:
    - active_backends:
      - SecretService Keyring
      - PlaintextKeyring with no encryption v.1.0 at /home/jdoe/.local/share/python_keyring/keyring_pass.cfg
    - config_file: /home/jdoe/.config/python_keyring/keyringrc.cfg
    - data_root: /home/jdoe/.local/share/python_keyring

The Keyring Python package also has its own CLI, which can report the
backends as well (different configuration shown)::

  $ keyring --list-backends
  keyring.backends.fail.Keyring (priority: 0)
  keyrings.alt.file.EncryptedKeyring (priority: 0.6)
  keyring.backends.chainer.ChainerBackend (priority: 10)
  keyrings.alt.file.PlaintextKeyring (priority: 0.5)

Some notable backends include:

- SecretService Keyring (``keyring.backends.SecretService.Keyring``):
  an interface to system daemons such as the GNOME Keyring and KDE
  Wallet. This one is the one most likely to be used on Linux
  desktops.
- EncryptedKeyring (``keyrings.alt.file.EncryptedKeyring``): passwords
  are stored in an encrypted text file. Provided by ``keyrings.alt``
  Python package but additionally requiring ``pycryptodomex`` to be
  installed.
- PlaintextKeyring (``keyrings.alt.file.PlaintextKeyring``): passwords
  are base64-encoded and stored in a plaintext file for which only the
  owner has read and write permissions. Provided by ``keyrings.alt``
  Python package.

Problem: Secret Service available but unusable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If GNOME Keyring is installed on a system, but a D-Bus session is not
started after login (the latter is likely to be the case on headless
systems), Keyring library sees the SecretService keyring as an
available backend and tries to use it, but fails with an error.

The error would appear for any operation requiring credential access
(e.g. ``datalad siblings enable``). Here we replicate it with the
``datalad credentials`` command (from DataLad-next)::

  $ datalad --log-level debug credentials
  (...)
  [DEBUG  ] Assigning credentials into 21 providers
  [DEBUG  ] Importing keyring
  [ERROR  ] Failed to create the collection: Prompt dismissed.


Problem: available backends change when activating a virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If a backend is provided by a Python package installed system-wide, it
may become "invisible" after activating a virtual environment which
lacks the package or its optional dependencies. In this case, DataLad
would not be able to access passwords saved previously with a given
backend, and would prompt for their entry (and then optionally store
them with another backend). The ``datalad wtf --section credentials``
listing would not include the unavailable backend.


User solution 1: configure preferred keyring
--------------------------------------------

Users can choose their default keyring backend.

The simplest option is a plaintext keyring, specified as
``keyrings.alt.file.PlaintextKeyring``. We will use it in our
examples. Other keyrings are available, but may require installing
`third-party packages`_.

.. _third-party packages: https://keyring.readthedocs.io/en/latest/?badge=latest#third-party-backends

A backend can be set through an environment variable (here affecting
only a single command call)::

  $ PYTHON_KEYRING_BACKEND=keyrings.alt.file.PlaintextKeyring datalad credentials

or by adding the following to the configuration file reported by
``datalad wtf`` (in our case: ``~/.local/share/python_keyring/keyring_pass.cfg``),
creating the file if needed:

.. code-block:: cfg

  [backend]
  default-keyring=keyrings.alt.file.PlaintextKeyring

.. note::

   With ``PlaintextKeyring``, credentials are written, base64-encoded,
   into a file for which only the owner has read and write permissions
   (``-rw-------``), but which is not protected otherwise. This may be
   sufficient for some setups and use cases, but is not recommended in
   general.


User solution 2: install required packages
------------------------------------------

If the problem is related to a Python library missing in the (virtual)
environment, it can be solved by installing it.

This is not always obvious. For example, the encrypted (file) keyring
is provided by ``keyrings.alt``, but is only active when an optional
dependency, ``pycryptodomex`` is present. Installing both will enable
it (by default with a higher priority than the plaintext
keyring). Python package for DataLad lists ``keyring`` and
``keyrings.alt`` as dependencies, but neither of them strictly depends
on ``pycryptodomex``, so the latter needs to be installed separately
[#]_.


User solution 3: start a D-bus session
--------------------------------------

Keyring library documentation provides another solution for `using
Keyring on headless Linux systems`_. It involves starting a D-Bus
session, and running ``gnome-keyring-daemon --unlock``, (which reads
unlock password via stdin). Follow instructions there.

.. _using keyring on headless linux systems: https://keyring.readthedocs.io/en/latest/?badge=latest#using-keyring-on-headless-linux-systems

Administrator solution: remove GNOME Keyring if not needed
----------------------------------------------------------

If the GNOME Keyring is not needed on the given system, its removal
will prevent Keyring library from trying to use it::

  # aptitude purge gnome-keyring

This will likely cause Keyring to use the plaintext keyring as a
backup; see note above for security considerations.


.. [#] interestingly, ``python3-keyrings.alt`` Debian package does
       depend on ``python3-pycryptodome``, at least as of version
       4.2.0-1. See:
       https://packages.debian.org/stable/python/python3-keyrings.alt
