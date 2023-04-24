.. index::
   double: datalad; clone; adjusted mode

.. highlight:: console

KBI0010: Cloning a dataset that exists in the form of an adjusted mode checkout
===============================================================================

:authors: Adina Wagner <adina.wagner@t-online.de>
:discussion: <link>
:keywords: adjusted mode, clone, cross-platform, Windows

Due to major difference between filesystems that git-annex regards a "crippled"
(such as those commonly found on `Windows machines`_ or smartphones) and common
file systems on Unix-like machines, cross-platform compatibility isn't always
easy to achieve.
This KBI details how one can clone a dataset that exists in the form of an
adjusted mode checkout to a Unix like machine.

.. _Windows machines: http://handbook.datalad.org/en/latest/intro/windows.html

Step by step demonstration
--------------------------

For the sake of this demonstration, a DataLad dataset is created on a FAT32 drive,
which simulated conditions similar to, e.g., a Windows computer::

    $ datalad create /media/mih/Samsung_T5/tmp/onwindows
    [INFO   ] Detected a filesystem without fifo support.
    [INFO   ] Disabling ssh connection caching.
    [INFO   ] Detected a crippled filesystem.
    [INFO   ] Entering an adjusted branch where files are unlocked as this filesystem does not support locked files.
    [INFO   ] Switched to branch 'adjusted/master(unlocked)'
    create(ok): /media/mih/Samsung_T5/tmp/onwindows (dataset)

To make the demo a bit more life-like, we save a file into that dataset::

   $ datalad run -d /media/mih/Samsung_T5/tmp/onwindows 'dd if=/dev/urandom bs=1M count=10 of={dspath}/big.dat'
   [INFO   ] == Command start (output follows) =====
   10+0 records in
   10+0 records out
   10485760 bytes (10 MB, 10 MiB) copied, 0.0254713 s, 412 MB/s
   [INFO   ] == Command exit (modification check follows) =====
   run(ok): /media/mih/Samsung_T5/tmp/onwindows (dataset) [dd if=/dev/urandom bs=1M count=10 of=/me...]
   add(ok): big.dat (file)
   save(ok): . (dataset)

Because this dataset is on a "crippled filesystem", git-annex operates in
`adjusted mode`_.
This means, among other things, that the files in the worktree are actual files
instead of symlinks, and that the dataset has an "adjusted/<branch>(unlocked)"
version of every branch::

    $ ls -l /media/mih/Samsung_T5/tmp/onwindows
    .rwxr-xr-x 10M mih mih 14 Apr 11:19 big.dat

When cloning this adjusted-mode checkout onto a Linux system, DataLad is not able
to establish a proper clone.
The clone will look like a dataset in adjust-mode, but it is not.
Putting the clone into adjusted-mode via `git-annex adjust --unlock` also does
not yield a working dataset.
To make things work, we simply remove the adjustment by checking out the regular
branch (usually, it would be called ``master`` or ``main``) and killing the
adjusted one::

    $  git -C /tmp/onlinux checkout master
    Switched to branch 'master'
    Your branch is up to date with 'origin/master'.
    $ git -C /tmp/onlinux branch -D adjusted/master\(unlocked\)
    Deleted branch adjusted/master(unlocked) (was 817e68f).

.. _adjusted mode: https://git-annex.branchable.com/design/adjusted_branches/