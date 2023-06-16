.. index::
   single: keyring; backends

.. highlight:: console

KBI0023: Keyring configuration
==============================

:authors: Michał Szczepanik
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/89
:keywords: keyring, credentials
:software-versions: datalad_0.18.3, datalad-next_0.6.3

This KBI covers keyring configuration in the context of a problem with
credential retrieval observed on a headless system. It also provides a
general overview of keyring access.

Problem description and troubleshooting
---------------------------------------

The problem manifested itself on any operation which requires
credential access (e.g. ``datalad siblings enable``). Here we
replicate it with a call to ``datalad credentials`` command (from
DataLad-next)::

  $ datalad --log-level debug credentials
  (...)
  [DEBUG  ] Assigning credentials into 21 providers
  [DEBUG  ] Importing keyring
  [ERROR  ] Failed to create the collection: Prompt dismissed..

This error is coming from the `Keyring`_ Python library, which is used
by DataLad to communicate with keyring backends available on the given
system.

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
      - PlaintextKeyring with no encyption v.1.0 at /home/jdoe/.local/share/python_keyring/keyring_pass.cfg
    - config_file: /home/jdoe/.config/python_keyring/keyringrc.cfg
    - data_root: /home/jdoe/.local/share/python_keyring

If GNOME Keyring is installed on a system, but a D-Bus session is not
started after login (which is likely to be the case on headless
systems), Keyring library sees the SecretService keyring as an
available backend and tries to use it, but fails with an error.

User solution 1: configure preferred keyring
--------------------------------------------

Users can choose their default keyring backend.

The simplest backend is a plaintext keyring, specified as
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

User solution 2: start a D-bus session
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
