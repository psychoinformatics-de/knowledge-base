.. index::
   single: RIA; dependency, 7zip, stalling

KBI0030: Stalling file retrieval from RIA stores due to missing 7z
==================================================================

:authors: Adina Wagner <adina.wagner@t-online.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/issues/119
:keywords: RIA, 7zip, file retrieval, stalling
:software-versions: datalad_0.19.3, git-annex_20221003

Until a re-write of the ``RIA`` functionality has been achieved (see `github.com/datalad/datalad-ria <https://github.com/datalad/datalad-ria>`_ for progress), certain RIA-related issues can be hard to pinpoint.
In cases where content in a RIA store has been compressed into `7-zip <https://7-zip.org/>`_ archives (:ref:`KBI 0024 <0024>` details instructions and benefits), it is important that `7-zip <https://7-zip.org/>`_ is installed and available on the machine hosting the RIA store.
Otherwise, file content retrieval via ``datalad get`` to a different machine can stall indefinitely and without any indication of an error.

An installation of ``7-zip`` is automatically included with some installation methods for ``datalad`` (for example when its installed as a `Debian package <https://handbook.datalad.org/en/latest/intro/installation.html#linux-neuro-debian-ubuntu-and-similar-systems>`_), but since the hosting machine of a RIA store does not need to have ``datalad`` installed, a stand-alone installation is suitable as well [1]_.

.. rubric:: Footnotes

.. [1] For example with miniconda (which works even on multi-user systems without needing elevated privileges):

       .. code-block::

          $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O shared/Miniconda3-latest-Linux-x86_64.sh
          $ bash shared/Miniconda3-latest-Linux-x86_64.sh -p ~/shared/miniconda3
          # An interactive installer will ask you to read and agree to the
          # license terms, and will ask you to confirm the installation location.
          # reply "yes" when asked whether to perform a conda init
          $ conda install -c conda-forge p7zip

