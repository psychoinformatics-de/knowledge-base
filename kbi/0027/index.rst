.. index::
   single: git-annex; transfer lock

KBI0027: "Transfer already in progress, or unable to take transfer lock"
========================================================================

:authors: Adina Wagner <adina.wagner@t-online.de>
:discussion: <link>
:keywords: transfer lock, datalad get, data retrieval
:software-versions: datalad_0.19.2, git-annex_10.20221003

When retrieving or uploading data, users can in rare cases see a failure together with the message ``Transfer already in progress, or unable to take transfer lock``.
This message originates in lock files git-annex uses to keep several transfer processes from interfering with each other.
Usually, it should suffice to wait a bit until the process that holds the lock open exits and releases the lock automatically.
But in some cases, e.g. when CTRL-C'ing a process unluckily or on Windows, the lock file can get stale, and the error message remains regardless of how long one waits.

When this happens, do the following:

- Be sure that there is no git-annex process that holds the lock open for a good reason. You should check the processes running on your system, and - when transferring data to a remote system - also the processes over there.

- If you are sure that the lock is stale, remove the files inside of ``.git/annex/transfer/``, and retry.

A short discussion for further reading can be found `here <https://git-annex.branchable.com/forum/How_to_fix__58_____40__transfer_already_in_progress__44___or_/>`_.

