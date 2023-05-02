.. index::
   single: git-annex; encryption

KBI0012: Annex encryption: fix passphrase prompt (GPG pinentry) not showing
===========================================================================

:authors: Michał Szczepanik <m.szczepanik@fz-juelich.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/44
:keywords: gnupg, gpg, encryption
:software-versions: datalad_0.18.1, gnupg_2.2.12

This technical note describes a solution to a specific issue related
to `encrypted git annex special remotes`_ that can be seen in certain
configurations (for example on a GNU/Linux machine with CLI access
only, or on a MacOS machine with fresh `GnuPG`_ installation from
Homebrew). For a use-case-style introduction to annex encryption with
DataLad, see `Encrypted data storage and transport`_ in the DataLad
Handbook.

Users who:

* use an encrypted git-annex special remote
* have no gpg-agent configuration
* use a passphrase-protected gpg key
* use a terminal-based pinentry program

.. _encrypted git annex special remotes: https://git-annex.branchable.com/encryption/
.. _gnupg: https://formulae.brew.sh/formula/gnupg
.. _encrypted data storage and transport: http://handbook.datalad.org/en/latest/usecases/encrypted_annex.html

may observe the following error when getting a file from an annex
remote that has encryption enabled:

.. code-block:: console

   $ datalad get foo.txt
   get(error): foo.txt (file) [user error (gpg ["--quiet","--trust-model","always","--batch","--decrypt"] exited 2)
   user error (gpg ["--quiet","--trust-model","always","--batch","--decrypt"] exited 2)

This happens because the gpg-agent called (by either DataLad or
git-annex) in a subprocess does not have a connection to the terminal
from which the ``get`` command was issued, and can not ask the user
for their GPG key passphrase. The problem does not occur if the
passphrase had been cached by gpg-agent.

It can be remedied by setting the ``GPG_TTY`` environment variable, as
explained by ``man gpg-agent``:

  You should always add the following lines to your ``.bashrc`` or
  whatever initialization file is used for all shell invocations:

  .. code-block:: bash

    GPG_TTY=$(tty)
    export GPG_TTY

For an alternative solution (that wasn't tested), it is likely
sufficient to have a graphical pinentry program (e.g. pinentry-mac on
MacOS, which can be installed with brew), and a pinentry program
option configured in ``~/.gnupg/gpg-agent.conf``:

.. code-block:: none

   pinentry-program $HOMEBREW_PREFIX/bin/pinentry-mac

