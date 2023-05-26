.. index::
   single: datalad;installation

KBI0020: Installing DataLad and dependencies in Google Colab
============================================================

:authors: Stephan Heunis <jsheunis@gmail.com>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/80
:keywords: Google Colab, Conda, installation```
:software-versions: datalad_0.18.4, git-annex_10.20230330-g98a3ba0ea, conda_23.3.1

Google Colaboratory allows anybody to write and execute arbitrary Python code
through the browser. It is particularly useful if you don't want to go through
the process of installing particular software on your local machine or server.

This knowledge base item summarizes suggested steps for installing DataLad and
all of its dependencies in a Google Colab notebook. `This blog post`_ was
particularly helpful to identify these steps:

- We suggest installation using ``conda``, specifically via ``miniconda``
- First, ``miniconda`` can be installed into a notebook environment using a
  Linux installer script, provided `here`_.
- Then, the environment's path variable has to be updated to include the
  location that ``conda`` installs packages into. This is necessary for Python to
  know where it can import available packages from.
- Lastly, ``datalad`` can be installed via ``conda`` per the
  `installation instructions`_.

An implementation of the above steps, with code and instructions, can be found
in this `Google Colab Notebook`_.

.. note::
  
  For standard notebook usage on Google Collaboratory, the installed
  software and data only remain available during a single runtime session. If
  a notebook is restarted, the software would have to be re-installed.

.. _here: https://docs.conda.io/en/latest/miniconda.html#linux-installers
.. _installation instructions: https://www.datalad.org/#install
.. _Google Colab Notebook: https://colab.research.google.com/drive/1SR-I-BDxQ5bHUKjABYI1Uu4HFlfDjOYE
.. _This blog post: https://towardsdatascience.com/conda-google-colab-75f7c867a522


