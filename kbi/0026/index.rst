.. index::
   single: configurations; shared repository

KBI0026: Passing configurations
===============================

:authors: Adina Wagner <adina.wagner@t-online.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/98
:keywords: configurations, shared repository clone
:software-versions: datalad_0.19.1, datalad-next_1.0.0b3, git_2.39.2

There are a variety of ways to configure datasets or DataLad operations.
This KBI documents relevant resources, and highlights a few special cases and relevant recent developments about them.

Existing resources
------------------

* A good introduction to the topic of configurations can be found in the `DataLad Handbook`_.
* An overview of Git-specific configurations can be found by running ``git help --config``, or in the `Git documentation`_.
* An overview of DataLad-specific configurations is in the `technical DataLad documentation`_.
* Specific documentation and examples for the ``datalad configuration`` command are in its `manpage`_. This command can be used to set, unset, or query configurations, and complements the capabilities of ``git config`` with, among other things, additional scopes or recursive operations.

.. _DataLad Handbook: https://handbook.datalad.org/en/latest/basics/basics-configuration.html
.. _Git documentation: https://git-scm.com/docs/git-config#_variables
.. _technical DataLad documentation: http://docs.datalad.org/en/stable/config.html
.. _manpage: http://docs.datalad.org/en/stable/generated/man/datalad-configuration.html


Recent developments
-------------------

In May 2023, a number of improvements to configuration handling were made in the DataLad extension ``datalad-next``.
They fix edge cases in the core ``datalad`` Python package.
The following paragraphs illustrate these edge cases for transparency, and a work-around requiring the use of environment variables.
At the time of writing though, an installation of `datalad-next`_ and the configuration ``datalad.extensions.load next``, as detailed in the project's documentation, would provide the necessary fixes to your DataLad installation to make the code function as expected.

Edge-cases in the core datalad package
**************************************

On a system with only the core ``datalad`` library installed, the ``-c/--configuration`` flag of the ``datalad`` main command displays a number of shortcomings for specific applications.
One of them is that configurations provided this way do not make it to the target process in every situation.

Here are two examples for configurations that do **not** get passed to the necessary subprocess:

**1) Configuring a different committer name:**
One could attempt to override the user name (``user.name`` Git config) of a specific ``save`` operation via

.. code-block::

   $ datalad -c user.name=someoneelse save

**2) Passing initialization configurations at cloning:**
Likewise, one could attempt to initialize a dataset as `"shared" <https://git-scm.com/docs/git-config#Documentation/git-config.txt-coresharedRepository>`_ in a ``datalad clone`` call::

   datalad -c core.sharedRepository=0600 \
    clone <source> <destination>``)

However, both cases would not yield the desired result.
Datalad or its sub-processes would continue to use the user name configured in the applicable ``.config`` file, and the ``core.sharedRepository=0600`` configuration would not be passed to the underlying internal ``git init`` process.
**Both code snippets would work as expected, however, if** `datalad-next`_ **is installed and loaded.**

Workaround: Environment variables
*********************************

A workaround without ``datlad-next`` requires the use of Git configurations in environment variables.
For example, in order to clone a dataset and initialize it as a shared repository without `datalad-next`_, the following environment variables need to be set (line breaks added for readability)::

    $ GIT_CONFIG_COUNT=1 \
      GIT_CONFIG_KEY_0=core.sharedRepository \
      GIT_CONFIG_VALUE_0=0600 \
      datalad clone <source> <destination>

.. _datalad-next: https://github.com/datalad/datalad-next/
.. _fixed: https://github.com/datalad/datalad-next/pull/399

