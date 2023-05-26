.. index::
   single: credentials;interactive authentication prompt

KBI0019: Workaround to an absent interactive authentication prompt
==================================================================

:authors: Stephan Heunis <jsheunis@gmail.com>
:discussion: https://github.com/psychoinformatics-de/knowledge-base/pull/79
:keywords: workaround, credentials, interactive authentication prompt, keyring
:software-versions: datalad_0.18.3

When retrieving file content for a dataset that requires authentication with credentials,
it could happen that DataLad's interactive authentication prompt does not appear as
expected and the process just stalls during a ``datalad get`` operation.

An example of such an issue is reported in
https://github.com/datalad/datalad/issues/7365.


Workaround
----------

While this does not solve the root cause, it has been identified that the local system's
keyring settings could be influencing the process. Disabling the keyring could
circumvent the issue. The keyring can be disabled by setting the environment variable:

.. code-block:: console

   export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring

This workaround should cause the credential prompt to be displayed correctly in response
to a ``datalad get``, and the file should be retrievable after entering the correct
credentials.

To delete this environment variable again, run ``unset PYTHON_KEYRING_BACKEND``.
