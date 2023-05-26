.. index::
   single: datalad; drop
   single: datalad; status

KBI0016: Drop local files added in a specific commit
====================================================

:authors: Stephan Heunis <jsheunis@gmail.com>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/66
:keywords: datalad status, datalad drop, git diff, scripting
:software-versions: datalad_0.18.3, git_2.39.1, 

In some cases it might be preferrable to drop file content from a DataLad dataset in local
storage after having pushed this content to a sibling of the dataset. This is particularly
useful in order to free up local storage space: since the data is now pushed safely to
remote storage, we don't have to store it locally anymore. However, a likely requirement
could be that only specific files should be dropped, for example all files that were added
to the dataset by a specific commit, while all other files that are available locally
should remain untouched.

This Knowledge Base Item outlines several methods for dropping local files that were added
in a specific commit. These methods differ in the way they identify which files to drop
(via ``datalad status``, ``git diff``, or ``datalad diff``), but the actual dropping of
content is handled by ``datalad drop`` in all cases.

Content
-------

- `Preparation`_
- `Using datalad status`_
- `Using git diff`_
- `Dropping the files`_
- `Using datalad diff in a one-liner`_
- `Drop limitation`_

.. note::
   If you are not interested in details and just looking for the quickest and leanest
   way to get the job done, skip over to the section: `Using datalad diff in a one-liner`_*.


.. _Preparation:

Preparation
-----------

Let's first create a DataLad dataset with the correct setup to support this demonstration.

.. code-block:: console

   datalad create drop-files-test
   create(ok): /Users/jsheunis/Documents/psyinf/Data/drop-files-test (dataset)

We can add some content to ensure that prior local content exists:

.. code-block:: console

   cd drop-files-test
   echo "file 1 content" > file1.txt
   
   datalad save -m "add file1 to the dataset"

   add(ok): file1.txt (file)
   save(ok): . (dataset)
   action summary:
      add (ok: 1)
      save (ok: 1)

After saving the dataset state, we can verify the specific commits in the git history:

.. code-block:: console

   git log

   commit 42f197501c3293bc1c0c22e36b1618eec706090e (HEAD -> main)
   Author: Stephan Heunis <s.heunis@fz-juelich.de>
   Date:   Wed May 10 21:50:27 2023 +0200

      add file1 to the dataset

   commit ba8266ccd88db5ae704e08b5f292c16748952026
   Author: Stephan Heunis <s.heunis@fz-juelich.de>
   Date:   Wed May 10 21:49:18 2023 +0200

      [DATALAD] new dataset
   
Let's also create and push to a sibling to ensure it exists and can be pushed to:

.. code-block:: console

   datalad create-sibling -s my-sibling ../my-sibling

   [INFO   ] Considering to create a target dataset /Users/jsheunis/Documents/psyinf/Data/drop-files-test at /Users/jsheunis/Documents/psyinf/Data/my-sibling of localhost
   [INFO   ] Fetching updates for Dataset(/Users/jsheunis/Documents/psyinf/Data/drop-files-test)
   update(ok): . (dataset)
   [INFO   ] Adjusting remote git configuration
   [INFO   ] Running post-update hooks in all created siblings
   create_sibling(ok): /Users/jsheunis/Documents/psyinf/Data/drop-files-test (dataset)

   datalad push --to my-sibling

   copy(ok): file1.txt (file) [to my-sibling...]
   publish(ok): . (dataset) [refs/heads/git-annex->my-sibling:refs/heads/git-annex 08856c6..ccfdb72]
   publish(ok): . (dataset) [refs/heads/main->my-sibling:refs/heads/main [new branch]]
   action summary:
      copy (ok: 1)
      publish (ok: 2)

Lastly, let's create more content in the dataset, this time without saving it (yet):

.. code-block:: console

   echo "the quick brown fox" > file2.txt
   echo "jumps over the lazy dog" > file3.txt


.. _Using datalad status:

Using ``datalad status``
------------------------

The first method that gives a view of what changed in the dataset is `datalad status`_,
an analog to ``git status``. By running this command, we can see which files are in the
``untracked`` state, which tells us which files we should drop after the push. Here we
show the state of the two files that were added last:

.. code-block:: console

   datalad status

   untracked: file2.txt (file)
   untracked: file3.txt (file)

The drawback of this approach is that it can't be done after the files have been committed
to ``git`` or ``git-annex`` (i.e. after running ``datalad save``), because then the files'
state would have changed to ``clean``, as with any other previously commited files in the
dataset.

In addition to ``datalad status``, other shell tools can also be used to streamline the
process. Below we use:

- ``jq`` to select only ``untracked`` files from the ``datalad status`` output, and
  then to extract the file paths
- ``xargs -I{} sh -c`` to run a shell command for each line in the output from ``jq``
- ``echo $(basename $1) >> "files_to_drop.out"`` to write the filename from each line
  above into an output file

.. code-block:: console

   datalad -f json status | jq '. | select(.state == "untracked") | .path' | xargs -I{} sh -c 'echo $(basename $1) >> "files_to_drop.out"' -- {}

Since we now have the list of files that we want to drop in an (untracked) file, we can
save the dataset and push the files to the remote sibling:

.. code-block:: console

   datalad save file2.txt file3.txt -m "save file2 and file3"

   add(ok): file2.txt (file)
   add(ok): file3.txt (file)
   save(ok): . (dataset)
   action summary:
      add (ok: 2)
      save (ok: 1)

   datalad push --to my-sibling

   copy(ok): file2.txt (file) [to my-sibling...]
   copy(ok): file3.txt (file) [to my-sibling...]
   publish(ok): . (dataset) [refs/heads/git-annex->my-sibling:refs/heads/git-annex 08856c6..ccfdb72]
   publish(ok): . (dataset) [refs/heads/main->my-sibling:refs/heads/main [new branch]]
   action summary:
      copy (ok: 2)
      publish (ok: 2)

.. _datalad status: https://docs.datalad.org/en/stable/generated/man/datalad-status.html


.. _Using git diff:

Using ``git diff``
------------------

`git diff`_ is a git command that can provide detailed information about the changes
between commits, branches, and more. If we know the commit hashes for the states before
and after the files were added, we can use this command to inspect the changed files.

By using ``git log``, we can find the specific commits:

.. code-block:: console

   git log

   commit 73489f56ecd5eb4dee14c957349f09c0d8b1684d (HEAD -> main, my-sibling/main)
   Author: Stephan Heunis <s.heunis@fz-juelich.de>
   Date:   Wed May 10 22:16:27 2023 +0200

      save file2 and file3
   
   commit 42f197501c3293bc1c0c22e36b1618eec706090e
   Author: Stephan Heunis <s.heunis@fz-juelich.de>
   Date:   Wed May 10 21:50:27 2023 +0200

      add file1 to the dataset

   commit ba8266ccd88db5ae704e08b5f292c16748952026
   Author: Stephan Heunis <s.heunis@fz-juelich.de>
   Date:   Wed May 10 21:49:18 2023 +0200

      [DATALAD] new dataset

This means:

- the files that we want to drop were added as part of commit ``73489f5...``
- the commit state before adding these files was ``42f1975...``

Now, we inspect ``git diff`` between the two commits (using ``..``), and we specify the
``--name-only`` flag so that it gives us only the filenames that changed between those
commits (i.e. not everything that changed inside these files):

.. code-block:: console

   git diff --name-only 42f197501c3293bc1c0c22e36b1618eec706090e..73489f56ecd5eb4dee14c957349f09c0d8b1684d > files_to_drop.out

   file2.txt
   file3.txt

Note: since we know that the commit with the added files is also the last commit (i.e. it
corresponds to the current ``HEAD``), we can also omit the second commit hash.

Let's write the filenames into an output file:

.. code-block:: console

   git diff --name-only 42f197501c3293bc1c0c22e36b1618eec706090e.. > files_to_drop.out

.. _git diff: https://git-scm.com/docs/git-diff


Dropping the files
------------------

Now we can again use some shell tools to streamline the dropping process.

Here we use:

- ``xargs -0 -n 1`` to execute a command once per line in the input file
- ``<<(tr \\n \\0 <files_to_drop.out)`` to supply the input file to ``xargs`` after
  using ``tr`` on the file to replace newline character with the ``\0`` character
  that ``xargs`` expects
- ``datalad -f json drop`` to drop the file provided by the ``xargs`` code

.. code-block:: console

   xargs -0 -n 1 datalad -f json drop <<(tr \\n \\0 <files_to_drop.out)

   {"action": "drop", "annexkey": "MD5E-s10--6fe97938d91d6a56a50c14caa5c81e12.txt", "path": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test/file2.txt", "refds": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test", "status": "ok", "type": "file"}
   {"action": "drop", "annexkey": "MD5E-s10--6fe97938d91d6a56a50c14caa5c81e12.txt", "path": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test/file3.txt", "refds": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test", "status": "ok", "type": "file"}


.. _Using datalad diff in a one-liner:

Using ``datalad diff`` in a one-liner
-------------------------------------

`datalad diff`_ provides similar information as ``git diff``, although with additonial
functionality related to (nested) DataLad datasets.

If you enjoy running one-liners and preventing unnecessary write operations to disk,
this option is for you. Below is a single line of code that uses ``datalad diff``, 
``datalad drop``, and standard UNIX tools to identify and drop files related to a
specific commit:

.. code-block:: console

   datalad drop $(datalad -f '{state}:{path}' diff -f HEAD~1 -t HEAD | grep '^added:' | cut -d ':' -f 2-)

To explain:

- ``-f 42f197501c3293bc1c0c22e36b1618eec706090e -t 73489f56ecd5eb4dee14c957349f09c0d8b1684d``
  uses ``datalad diff``'s ``--from`` and ``--to`` options to specify the two states that
  will be compared (here using the commit shasums). Alternatively, symbolic names could
  also be used, for example ``-f HEAD~1 -t HEAD`` to refer to the last commit.
- ``-f '{state}:{path}'`` uses DataLad's custom formatting option to format results of
  the ``datalad diff`` command. It produces output like
  ``added::/Users/jsheunis/Documents/psyinf/Data/drop-files-test/file2.txt``.
- ``grep`` and ``cut`` are standard UNIX tools to find lines that start with ``added:``,
  and to only report on the path that is contained in these lines.

This approach could be extended to also cover files that were modified in a specific
commit, by merely amending the ``grep`` part of the command to grep ``'^modified:'``.

.. _datalad diff: https://docs.datalad.org/en/stable/generated/man/datalad-diff.html


Congrats! You now know multiple ways to drop local files that were added in a specific
commit!

.. _Drop limitation:

Drop limitation
---------------

All of the above examples use a path-based approach to ``drop`` content, although this
has a specific limitation if the relevant file path was removed in an earlier commit.
This means there is no actual file in the worktree, and ``datalad drop <path-to-file>``
would result in an error. To address this, we can let ``datalad diff`` report annex keys
instead of paths, and use `git annex drop`_ to drop the content:

.. code-block:: console

   datalad -f '{state}:{key}' diff --annex -f HEAD~1 -t HEAD | grep -v '^clean:' | cut -d ':' -f 2- | git annex drop --batch-keys

To explain:

- ``datalad diff``'s ``--from`` and ``--to`` options are used here to find the files that
  changed during the last commit (``-f HEAD~1 -t HEAD``).
- ``-f '{state}:{path}'`` is used in the same way as before
- ``grep -v '^clean:'`` is used with the invert the matching of lines, i.e. it selects
  all lines where the state is *not* ``clean``
- ``cut`` is used in the same way as before
- ``git annex drop --batch-keys`` tells git-annex to drop files specified by the incoming
  annex keys

.. _git annex drop: https://git-annex.branchable.com/git-annex-drop/