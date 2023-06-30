.. index::
   single: configurations; shared repository

KBI0026: Passing configurations
===============================

:authors: Adina Wagner <adina.wagner@t-online.de>
:discussion: <link>
:keywords: configurations, shared repository clone
:software-versions: datalad_0.19.1, datalad-next_1.0.0b3, git_2.39.2

There are a variety of ways to configure datasets or DataLad operations.
This KBI documents relevant resources, and highlights a few special cases and relevant recent developments about them.

Existing resources
------------------

* A good introduction into the topic of configurations is in the `DataLad Handbook`_.
* An overview of Git-specific configurations can be found by running ``git help --config``, or in the `Git documentation`_.
* An overview of DataLad-specific configurations is in the `technical DataLad documentation`_.
* Specific documentation and examples for the ``datalad configuration`` command are in its `manpage`_. This command can be used to set, unset, or query configurations, and complements the capabilities of ``git config`` with, among other things, additional scopes or recursive operations.

.. _DataLad Handbook: https://handbook.datalad.org/en/latest/basics/basics-configuration.html
.. _Git documentation: https://git-scm.com/docs/git-config#_variables
.. _technical DataLad documentation: http://docs.datalad.org/en/stable/config.html
.. _manpage: http://docs.datalad.org/en/stable/generated/man/datalad-configuration.html


Recent developments
-------------------

The ``-c/--configuration`` flag of the ``datalad`` main command displays a number of shortcomings for specific applications.
One of them is that configurations provided this way do not make it to the target process in every situation.
For example, an attempt to override the user name (``user.name`` Git config) via ``datalad -c user.name=someoneelse save`` would be unsuccessful, and continued to use the user name configured in the applicable ``.config`` file.
This shortcoming was `fixed`_ in May 2023.
At the time of writing, and the fix can be enabled with an installation of `datalad-next`_ and the configuration ``datalad.extensions.load next``, as detailed in the projects documentation.

The alternative workaround requires the use of Git configurations in environment variables.
For example, in order to clone a dataset and initialize it as a shared repository, the following call would only work when `datalad-next`_ is installed and loaded (line breaks added for readability)::

    $ datalad -c core.sharedRepository=0600 \
      clone <source> <destination>

Without `datalad-next`_, it would succeed with the following environment variables (line breaks added for readability)::

    $ GIT_CONFIG_COUNT=1 \
      GIT_CONFIG_KEY_0=core.sharedRepository \
      GIT_CONFIG_VALUE_0=0600 \
      datalad clone <source> <destination>

.. _datalad-next: https://github.com/datalad/datalad-next/
.. _fixed: https://github.com/datalad/datalad-next/pull/399

