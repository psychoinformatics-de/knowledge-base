import os
import sys

from datalad_dataverse.utils import get_native_api
from datalad_next.datasets import Dataset

# API token is specified via the environment
dvtoken = os.environ['DATAVERSE_API_TOKEN']

# the two positional arguments at the dataverse instance base URL
# and the PID of the dataset
dvurl = sys.argv[1]
dvds_pid = sys.argv[2]

api = get_native_api(dvurl, dvtoken)

# get info and file listing for the latest version of that dataset
dslisting = api.get_dataset(
    dvds_pid,
    version=':latest',
).json()['data']['latestVersion']

# this produces a list of dicts, where each dict represents a single
# file in the dataset, and all relevant keys are accessible directly
# at the top-level. The original structure is more complex (nested)
dsfiles = [
    dict(
        f,
        directory=f.get('directoryLabel', '.'),
        sha265=f['dataFile']['checksum']['value'],
        **f['dataFile'])
    for f in dslisting['files']
]

dlds = Dataset('.')

# feed file info to datalad's addurls
# this call assumes that the dataverse instance is reporting
# SHA256 checksums (other checksums could be used if available).
# being able to define a git-annex key from the metadata alone
# makes it possible to generate the dataset content without
# having to download any file.
dlds.addurls(
    urlfile=dsfiles,
    urlformat=f'{dvurl}/api/access/datafile/{{id}}',
    filenameformat='{directory}/{label}',
    key='et:SHA256-s{filesize}--{sha256}',
    exclude_autometa='*',
    fast=True,
    save=False,
)
