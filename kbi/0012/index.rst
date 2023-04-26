.. index::
   single: git-annex; encryption

KBI0012: Annex encryption & gpg pinentry
========================================

:authors: Michał Szczepanik <m.szczepanik@fz-juelich.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/44
:keywords: gnupg, gpg, encryption
:software-versions: datalad_0.18.1, gnupg_2.2.12

Users who:

* use an `encrypted`_ git-annex special remote
* have no gpg-agent configuration
* use a password-protected gpg key
* use a terminal-based pinentry program

(for example GNU/Linux users with CLI access only, or MacOS users with
fresh `GnuPG`_ installation from Homebrew)

.. _encrypted: https://git-annex.branchable.com/encryption/
.. _gnupg: https://formulae.brew.sh/formula/gnupg

may observe the following error when getting a file from an annex
remote that has encryption enabled:

.. code-block:: console

   $ datalad get foo.txt
   get(error): foo.txt (file) [user error (gpg ["--quiet","--trust-model","always","--batch","--decrypt"] exited 2)
   user error (gpg ["--quiet","--trust-model","always","--batch","--decrypt"] exited 2)

This happens because the gpg-agent called (by either DataLad or
git-annex) in a subprocess does not have a connection to the terminal
from which the ``get`` command was issued. It can be remedied by
setting the ``GPG_TTY`` environment variable, as explained by ``man
gpg-agent``:

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

