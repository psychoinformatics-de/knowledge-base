.. index::
   single: RIA; cross-platform
   single: datalad-next; RIA

KBI0032: Pushing to RIA-store between OSs, and other improvements
=================================================================

:authors: Michał Szczepanik <m.szczepanik@fz-juelich.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/125
:keywords: datalad-next, RIA, macOS, linux, windows, cross-platform
:software-versions: datalad-next_1.4.1, datalad_1.0.2

DataLad versions prior to 1.1.2 can display the
following error when pushing to a RIA store from macOS to a linux
server [#f2]_:

.. code-block:: none

   Unable to remove <remote-store-path>/...//.../transfer/<annex-key> or to obtain write permission in parent directory. -caused by- stat -f%Dp <remote-store-path>/...//.../transfer failed:
   copy: 1 failed

This can be translated as: DataLad tried to execute the ``stat``
command on Linux, with macOS-specific parameterization (``-f%Dp``).

A fix, together with a set of other improvements to to the RIA
functionality of DataLad, has been released in the DataLad-next
extension, in v.1.4.1 (`changelog`_).

Additionally, the 1.4 release of DataLad-next replaces most of the RIA
implementation, including the ORA special remote, and the
create-sibling-ria command. The new implementation brings uniform
support for Windows clients, progress reporting for uploads and
downloads via SSH, and a faster and more robust behavior for SSH-based
operations (from `changelog`_).

`DataLad-next`_ is a separate Python package (`DataLad extension`_),
and can be installed e.g. with ``pip``. It is also available as a
Debian package [#f3]_. It needs to be enabled (``git
config --global --add datalad.extensions.load next``) after
installation to allow it to override default DataLad behavior.

.. rubric:: Footnotes
.. [#f2] Reported e.g. in this `GitHub issue`_ and this `Neurostars
         thread`_, which prompted this KBI.
.. [#f3] At the moment of writing, the latest version available in
         Debian stable is 1.2.0, which does not contain a fix to the
         issues described above.

.. _changelog: https://github.com/datalad/datalad-next/blob/main/CHANGELOG.md#140-2024-05-17
.. _DataLad-next: https://docs.datalad.org/projects/next/en/latest/
.. _pull request: https://github.com/datalad/datalad/pull/7549
.. _GitHub issue: https://github.com/datalad/datalad/issues/7536
.. _Neurostars thread: https://neurostars.org/t/datalad-push-to-ria-storage-not-working/29049
.. _DataLad extension: https://handbook.datalad.org/en/latest/extension_pkgs.html
