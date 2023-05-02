.. index::
   single: installation; datalad
   single: installation; extensions

KBI0011: Debugging installation issues related to multiple Python versions
==========================================================================

:authors: Michał Szczepanik <m.szczepanik@fz-juelich.de>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/43
:keywords: python version, package manager, pip, conda, MacOS, linux, Windows
:software-versions: datalad_0.18.3, python_3.9.2

It is not uncommon to have multiple Python versions installed on a
single machine. It can be needed, for example, when using several
software stacks with different requirements (some programs can even
come with their own Python installation). `Virtual environments`_ and
`conda environments`_ are two popular methods of managing multiple
versions of Python packages and / or Python itself.

DataLad is a Python package which also provides a command line
interface (``datalad`` command). DataLad can be installed with
different methods, including package managers such as ``apt``,
``homebrew``, ``conda``, ``pip``, or others, depending on user
preferences. DataLad extensions are also distributed through different
channels, but are most commonly installed using ``pip``, the package
installer for Python [#f1]_.

Like with any other command line tool, the actual executable used when
calling the ``datalad`` command is determined by searching several
locations in the order determined by the `PATH variable`_. If DataLad
is installed in several locations (e.g. different Python versions or
multiple virtual environments), the installation used in a given
moment will be dependent on current ``PATH`` (affected by system
settings, user settings, and potentially modified by an active virtual
environment).

In certain situations, the resolution order may lead to unexpected
DataLad configurations, for example when the ``datalad`` command is
provided in one Python installation, but ``pip`` comes from another,
or if an older Python version takes precedence in ``PATH``. In the
latter case, a seemingly fresh DataLad install may provide an outdated
version (DataLad roughly follows the `Python release cycle`_; e.g.,
support for Python 3.6 has been dropped in DataLad 0.16).

This KBI presents examples of two such installation issues, and
discusses simple and useful debugging steps.

.. _virtual environments: https://docs.python.org/3/library/venv.html
.. _conda environments: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
.. _PATH variable: https://en.wikipedia.org/wiki/PATH_(variable)
.. _Python release cycle: https://devguide.python.org/versions/

Examples
--------

Conda competing with Homebrew on MacOS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On MacOS, DataLad had been installed with homebrew. Conda base
environment was activated by default. Datalad-Next had been installed
with pip install. Problems were observed when cloning a datalad-annex
URL (handling of which should be provided by DataLad-Next):

.. code-block:: console

  $ datalad clone "datalad-annex::(...)"
  [WARNING] Requested extension 'next' is not available 
  install(error): (...)
  [ERROR  ] Cannot handle URL 'datalad-annex::(...)'
  $ python -m pip install datalad-next
  Requirement already satisfied: datalad-next in /Users/jdoe/opt/anaconda3/lib/python3.9/site-packages (0.6.3)

In this instance, it turned out that although the conda environment
was activated (and pip installed both DataLad and DataLad-next into
that environment), the homebrew-installed DataLad was higher in the
``PATH``. Because the user preferred working with that conda environment,
the problem was resoved by uninstalling homebrew-DataLad and relying
on conda to provide DataLad and DataLad-Next.

Conflicting Python versions on Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python 3.11 was installed on a Windows machine where PsychoPy had been
previously used. After installing Python 3.11, DataLad and
DataLad-next were installed with ``pip install datalad datalad-next``.

Problems manifested when trying to use the ``create-sibling-webdav``
command (provided by DataLad-Next):

.. code-block:: console

  $ datalad create-sibling-webdav ...
  Traceback (most recent call last):
  (...)
  ModuleNotFoundError: No module named 'datalad.distributed.create_sibling_ghlike'

Inspecting the diagnostic output revealed that standalone Python 3.6
installed with PsychoPy in ``C:\Program Files\PsychoPy3`` was higher
in ``PATH`` then Python 3.11 from ``AppData\Local``. Calling ``pip
install`` installed packages under Python 3.6, causing installation of
an outdated DataLad version, and a non-functional DataLad-Next. These
are excerpts from a diagnostic output:
  
.. code-block:: console

  $ datalad wtf
  # WTF
  ## datalad
    - version: 0.15.6
  ## extensions
    - next:
      - load_error: ModuleNotFoundError(No module named 'datalad.distributed.create_sibling_ghlike')
  ## python
    - implementation: CPython
    - version: 3.6.6

Because PsychoPy was not actively used on that machine, the issue was
resolved by editing the PATH variable.


How to check DataLad installation
---------------------------------

The simplest way to start is by checking if the reported DataLad
version matches expectations.

.. code-block:: console

  $ datalad --version
  datalad 0.18.3

Another useful check is to see where the ``datalad`` command is
actually coming from. This can be done using ``which`` (Unix-like
shells), ``where`` (Windows CMD), or ``Get-Command`` (PowerShell)
command. The example below comes from a Debian system where DataLad
was installed with ``apt`` system package manager:

.. code-block:: console

  $ which datalad
  /usr/bin/datalad

The output changes after activating a virtual environment called
"example" (done here with `virtualenvwrapper`_) in which DataLad had
been previously installed:

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io

.. code-block:: console

  $ workon example
  $ which datalad
  /home/jdoe/.virtualenvs/example/bin/datalad

The ``which`` command (or its equivalents) can be used for any other
program, including ``pip``:

.. code-block:: console

  $ which pip
  /home/jdoe/.virtualenvs/example/bin/

The most comprehensive information can be found in the output of the
``datalad wtf`` diagnostic command. The output has many sections,
which can also be viewed individually with the ``--section``
argument. The most relevant sections in the context of installation
are listed below.

DataLad version:

.. code-block:: console

  $ datalad wtf --section datalad
  # WTF
  ## datalad 
    - version: 0.18.3

Python version:
      
.. code-block:: console

  $ datalad wtf --section python    
  # WTF
  ## python 
    - implementation: CPython
    - version: 3.9.2

Important environment variables, including PATH. Path is usually a
single long line with components separated by ``:``; in the output
below they have been moved to separate lines for readability. Note
that since this was done in the virtual environment mentioned above,
the virtual environment path is first on the list, and takes
precedence over ``/usr/bin`` where the installation available outside
the virtualenv is located.

.. code-block:: console

  $ datalad wtf --section environment
  # WTF
  ## environment 
    - LANG: en_US.UTF-8
    - LANGUAGE: en_US.UTF-8
    - LC_ALL: en_US.UTF-8
    - LC_CTYPE: en_US.UTF-8
    - PATH:
      /home/jdoe/.virtualenvs/example/bin:
      /usr/local/sbin:
      /usr/local/bin:
      /usr/sbin:
      /usr/bin:
      (...)
      /home/jdoe/texlive/2022/bin/x86_64-linux:

Finally, the list of extensions (available in the currently used installation):
      
.. code-block:: console

  $ datalad wtf --section extensions
  # WTF
  ## extensions
    (...)
    - next: 
      - description: What is next in DataLad
      - entrypoints:
  
        (...)

      - load_error: None
      - module: datalad_next
      - version: 1.0.0b2
   (...)

The Datalad Handbook has a nice and more general section on inspecting
errors and reading the diagnostic output: `How to get help`_.

.. _how to get help: https://handbook.datalad.org/en/latest/basics/101-135-help.html

.. rubric:: Footnotes

.. [#f1] The name pip originated as an `acronym and declaration`_: pip
         installs packages.

.. _acronym and declaration: https://ianbicking.org/blog/2008/10/pyinstall-is-dead-long-live-pip.html
