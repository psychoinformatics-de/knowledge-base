.. index::
   single: datalad; RIA
.. highlight:: console

KBI0029: Create an empty RIA store
==================================

:authors: Laura Waite <laura@waite.eu>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/110
:keywords: RIA store
:software-versions: datalad_0.19.3

To create a `RIA store`_, the most common workflow is to execute the command
``create-sibling-ria`` within an existing DataLad dataset. However, if desired,
it is possible to setup an empty RIA store without requiring an existing
DataLad dataset. All that is needed is a directory for the store, the
``ria-layout-version`` file , and the ``error-logs`` directory. This structure
can be created by hand, or alternatively, using the helper function
``create_store`` in ``datalad/customremotes/ria_utils.py``.

Examples
--------

Set up by hand::

  $ cd /tmp
  $ mkdir -p mock_ria/error_logs
  $ echo "1" > mock_ria/ria-layout-version

Helper function (ipython or script)::

  from pathlib import PurePosixPath
  from datalad.customremotes.ria_utils import create_store
  from datalad.distributed.ora_remote import SSHRemoteIO

  ssh_host = "ssh://example.com"
  base_path = PurePosixPath("/path/to/mock_ria")

  create_store(
      io=SSHRemoteIO(ssh_host),  # or LocalIO()
      base_path=base_path,
      version="1",
  )

Either of the above examples should result in::

  $ tree mock_ria
  mock_ria
  ├── error_logs
  └── ria-layout-version

  $ cat mock_ria/ria-layout-version
  1

And that's it! ``mock_ria`` is now a valid (and empty) RIA store.

To demonstrate, we can create a new dataset and add the new RIA store as a sibling::

  $ datalad create my_dataset && cd my_dataset
  create(ok): /tmp/my_dataset (dataset)

  $ echo 12435 > file.txt && datalad save
  add(ok): file.txt (file)
  save(ok): . (dataset)
  action summary:
    add (ok: 1)
    save (ok: 1)

  $ datalad create-sibling-ria 'ria+file:///tmp/mock_ria' -s ria --alias my_dataset
  [INFO   ] create siblings 'ria' and 'ria-storage' ...
  [INFO   ] Fetching updates for Dataset(/tmp/my_dataset)
  update(ok): . (dataset)
  update(ok): . (dataset)
  [INFO   ] Configure additional publication dependency on "ria-storage"
  configure-sibling(ok): . (sibling)
  create-sibling-ria(ok): /tmp/my_dataset (dataset)
  action summary:
    configure-sibling (ok: 1)
    create-sibling-ria (ok: 1)
    update (ok: 1)
  0.00 [00:00, ?/s]

  $ datalad push --to ria
  copy(ok): file.txt (file) [to ria-storage...]
  publish(ok): . (dataset) [refs/heads/master->ria:refs/heads/master [new branch]]
  publish(ok): . (dataset) [refs/heads/git-annex->ria:refs/heads/git-annex [new branch]]
  action summary:
    copy (ok: 1)
    publish (ok: 2)

  $ cd ../
  $ datalad clone 'ria+file:///tmp/mock_ria#~my_dataset' newclone
  [INFO   ] Configure additional publication dependency on "ria-storage"
  configure-sibling(ok): . (sibling)
  install(ok): /tmp/newclone (dataset)
  action summary:
    configure-sibling (ok: 1)
    install (ok: 1)

  $ cd newclone
  $ datalad get file.txt
  get(ok): file.txt (file) [from ria-storage...]


.. _ria store: http://handbook.datalad.org/en/latest/beyond_basics/101-147-riastores.html
