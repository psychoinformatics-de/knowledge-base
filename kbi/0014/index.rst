.. index::
   single: datalad push; tags

KBI0014: Pushing tags with ``datalad push``
===========================================

:authors: Michael Hanke <michael.hanke@gmail.com>, Stephan Heunis <jsheunis@gmail.com>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/52
:keywords: datalad push, tags, git config
:software-versions: datalad_0.18.3, git_2.39.1

The `datalad push`_ command makes a saved state of a dataset available to a sibling, both
in terms of the dataset's git repository and its annex. Internally, the command uses `git push`_
and ``git annex copy`` to push a dataset state to a sibling. Importantly, it honors the configuration
of ``git push`` by allowing users to specify e.g. *what* to push, which could include the repository tags.
This implies that if the datalad dataset (i.e. git repository) is configured via `git config`_
to include tags in the push operation, the ``datalad push`` command will result in the tags being pushed
to the sibling.

The example code below demonstrates how to configure a dataset's so-called `refspec <https://git-scm.com/book/en/v2/Git-Internals-The-Refspec>`_
to include tags, and what the result of ``datalad push`` looks like.

.. _datalad push: https://handbook.datalad.org/en/latest/basics/101-141-push.html
.. _git push: https://git-scm.com/docs/git-push
.. _git config: https://git-scm.com/docs/git-config

Example
-------

First create a demo dataset:

.. code-block:: console

   $ datalad create ds

Then create a demo remote repository:

.. code-block:: console

   $ mkdir remote
   $ git -C remote init --bare

Now we register the remote in the dataset:

.. code-block:: console

   $ datalad siblings -d ds add -s origin --url /tmp/push/remote/

And update the dataset's configuration:

.. code-block:: console

   # configure all branches to be pushed by default
   $ git -C ds config --add remote.origin.push 'refs/heads/*'
   # configure all tags to be pushed by default too
   $ git -C ds config --add remote.origin.push 'refs/tags/*'

Finally, we can add a tag to the dataset and test the push operation:

.. code-block:: console

   # add a tag to the dataset
   $ git -C ds tag mytag
   # push
   $ datalad push -d ds --to origin
   publish(ok): . (dataset) [refs/heads/git-annex->origin:refs/heads/git-annex [new branch]]
   publish(ok): . (dataset) [refs/heads/master->origin:refs/heads/master [new branch]]
   publish(ok): . (dataset) [refs/tags/mytag->origin:refs/tags/mytag [new tag]]