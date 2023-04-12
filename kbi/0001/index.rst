.. index::
   single: clone; multiple users

KBI0001: Shared (multi-user) Git clones
=======================================

:authors: Michał Szczepanik <m.szczepanik@fz-juelich.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/1
:keywords: shared, clone, safe.directory

Overview
--------

Some users who want to clone Git repositories (DataLad datasets) from locations on a machine that are owned by other users
report receiving an error message saying that they should consider
setting a ``safe.directory`` git config option (possibly affects only
cloning from checked-out datasets, not sure about bare repositories
created as part of RIA). This technical note provides background
information about the observed behavior, and guidance on possible solutions.

Git version 2.35.2 introduced checks for the top-level directory
ownership, and a ``safe.directory`` config option to to bypass these
checks. Description of the config option can be found in `git config
docs <https://git-scm.com/docs/git-config>`__ (Ctrl-F
``safe.directory``), and begins as follows:

   These config entries specify Git-tracked directories that are
   considered safe even if they are owned by someone other than the
   current user. By default, Git will refuse to even parse a Git config
   of a repository owned by someone else, let alone run its hooks, and
   this config setting allows users to specify exceptions, e.g. for
   intentionally shared repositories (see the –shared option in
   git-init). (…)

Related GitHub blog post:
https://github.blog/2022-04-12-git-security-vulnerability-announced/

Further background
------------------

These are relevant fragments from Git v2.35.2 and v2.30.2 release
notes (note that changes released in 2.35.2 were also applied to older
maintenance tracks):

::

   Git v2.35.2 Release Notes
   =========================

   This release merges up the fixes that appear in v2.30.3,
   v2.31.2, v2.32.1, v2.33.2 and v2.34.2 to address the security
   issue CVE-2022-24765; see the release notes for these versions
   for details.

   Git v2.30.2 Release Notes
   =========================

   This release addresses the security issue CVE-2022-24765.

   Fixes since v2.30.2
   -------------------

    * Build fix on Windows.

    * Fix `GIT_CEILING_DIRECTORIES` with Windows-style root directories.

    * CVE-2022-24765:
      On multi-user machines, Git users might find themselves
      unexpectedly in a Git worktree, e.g. when another user created a
      repository in `C:\.git`, in a mounted network drive or in a
      scratch space. Merely having a Git-aware prompt that runs `git
      status` (or `git diff`) and navigating to a directory which is
      supposedly not a Git worktree, or opening such a directory in an
      editor or IDE such as VS Code or Atom, will potentially run
      commands defined by that other user.

   Credit for finding this vulnerability goes to 俞晨东; The fix was
   authored by Johannes Schindelin.

A message for the commit which introduced the change to Git [1]_ is
more verbose about the reasons - notably mentioning educational
institutes as an example:

::

   commit 8959555cee7ec045958f9b6dd62e541affb7e7d9
   Author: Johannes Schindelin <Johannes.Schindelin@gmx.de>
   Date:   Wed Mar 2 12:23:04 2022 +0100

       setup_git_directory(): add an owner check for the top-level directory
       
       It poses a security risk to search for a git directory outside of the
       directories owned by the current user.
       
       For example, it is common e.g. in computer pools of educational
       institutes to have a "scratch" space: a mounted disk with plenty of
       space that is regularly swiped where any authenticated user can create
       a directory to do their work. Merely navigating to such a space with a
       Git-enabled `PS1` when there is a maliciously-crafted `/scratch/.git/`
       can lead to a compromised account.
       
       The same holds true in multi-user setups running Windows, as `C:\` is
       writable to every authenticated user by default.
       
       To plug this vulnerability, we stop Git from accepting top-level
       directories owned by someone other than the current user. We avoid
       looking at the ownership of each and every directories between the
       current and the top-level one (if there are any between) to avoid
       introducing a performance bottleneck.
       
       This new default behavior is obviously incompatible with the concept of
       shared repositories, where we expect the top-level directory to be owned
       by only one of its legitimate users. To re-enable that use case, we add
       support for adding exceptions from the new default behavior via the
       config setting `safe.directory`.
       
       The `safe.directory` config setting is only respected in the system and
       global configs, not from repository configs or via the command-line, and
       can have multiple values to allow for multiple shared repositories.
       
       We are particularly careful to provide a helpful message to any user
       trying to use a shared repository.

Later changes, citing feedback from users who have a very large list of
shared repositories, introduced the possibility to set the value of the
config option to ``*``, implying that all directories are safe.

Recommendation
--------------

Taking into consideration the information above, DataLad users should
use their own judgment in setting the ``safe.directory`` config option.

.. [1]
   Found by ``git log Documentation/config/safe.txt`` in a clone of git
   repository; can be also seen in
   https://github.com/git/git/commits/v2.37.0/Documentation/config/safe.txt
