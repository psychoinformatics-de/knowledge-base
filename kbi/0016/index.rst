.. index::
   single: datalad; drop
   single: datalad; status

KBI0016: Drop local files added in a specific commit
====================================================

:authors: Stephan Heunis <jsheunis@gmail.com>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/65
:keywords: datalad status, datalad drop, git diff, scripting
:software-versions: datalad_0.18.3, git_2.39.1, 


In some cases it might be preferrable to drop file content from a DataLad dataset in local
storage after having pushed this content to a sibling of the dataset. This is particularly
useful in order to free up local storage space: since the data is now pushed safely to
remote storage, we don't have to store it locally anymore. However, a likely requirement
could be that only specific files should be dropped, for example all files that were added
to the dataset by a specific commit, while all other files that are available locally
should remain untouched.

This Knowledge Base Item outlines two methods for dropping local files that were added in
a specific commit. These methods differ in the way they identify which files to drop (one
via ``datalad status`` and one via ``git diff``), but the actual dropping of content is
handled in the same way.

Preparation
-----------

.. code-block:: console

   datalad create drop-files-test
   create(ok): /Users/jsheunis/Documents/psyinf/Data/drop-files-test (dataset)
   
   cd drop-files-test
   echo "file 1 content" > file1.txt
   
   datalad save -m "add file1 to the dataset"
   add(ok): file1.txt (file)
   save(ok): . (dataset)
   action summary:
      add (ok: 1)
      save (ok: 1)
   
   git log
   commit 42f197501c3293bc1c0c22e36b1618eec706090e (HEAD -> main)
   Author: Stephan Heunis <s.heunis@fz-juelich.de>
   Date:   Wed May 10 21:50:27 2023 +0200

      add file1 to the dataset

   commit ba8266ccd88db5ae704e08b5f292c16748952026
   Author: Stephan Heunis <s.heunis@fz-juelich.de>
   Date:   Wed May 10 21:49:18 2023 +0200

      [DATALAD] new dataset
   
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


   echo "the quick brown fox" > file2.txt
   echo "jumps over the lazy dog" > file3.txt
   


Using ``datalad status``
------------------------

`datalad status`_ (an analog to ``git status``)

.. code-block:: console

   datalad status
   untracked: file2.txt (file)
   untracked: file3.txt (file)

   datalad -f json status
   {"action": "status", "parentds": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test", "path": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test/file2.txt", "refds": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test", "state": "untracked", "status": "ok", "type": "file"}
   {"action": "status", "parentds": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test", "path": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test/file3.txt", "refds": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test", "state": "untracked", "status": "ok", "type": "file"}

   datalad -f json status | jq '. | select(.state == "untracked") | .path' | xargs -I{} sh -c 'echo $(basename $1) >> "files_to_drop.out"' -- {}

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

Using ``git diff``
------------------

`git diff`_

.. code-block:: console
   git diff --name-only 42f197501c3293bc1c0c22e36b1618eec706090e.. > files_to_drop.out


.. _git diff: https://git-scm.com/docs/git-diff


Finally, dropping the files
---------------------------

.. code-block:: console

   xargs -0 -n 1 datalad -f json drop <<(tr \\n \\0 <files_to_drop.out)
   {"action": "drop", "message": "no annex'ed content", "path": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test/file2.txt", "refds": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test", "status": "notneeded", "type": "file"}
   {"action": "drop", "message": "no annex'ed content", "path": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test/file3.txt", "refds": "/Users/jsheunis/Documents/psyinf/Data/drop-files-test", "status": "notneeded", "type": "file"}