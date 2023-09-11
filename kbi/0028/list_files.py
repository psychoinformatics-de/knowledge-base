import csv
from pathlib import PurePosixPath

from datalad.api import credentials
from webdav4.fsspec import WebdavFileSystem

# Retrieve Nextcloud credentials from DataLad
cred = credentials(
    "get",
    name="webdav-mycred",
    return_type="item-or-list",
)

# Create a fsspec filesystem object, with user's Nextcloud home as root
fs = WebdavFileSystem(
    "https://example.com/nextcloud/remote.php/dav/files/USERNAME/",
    auth=(cred["cred_user"], cred["cred_secret"]),
)

# Shared directory, contents of which should be listed
DIRNAME = "sharing/example"

# List files in the shared directory, writing outputs to a csv file for addurls
with open("listing.csv", "wt") as urlfile:
    writer = csv.writer(urlfile, delimiter=",")
    writer.writerow(["name", "href"])

    for dirpath, dirinfo, fileinfo in fs.walk(DIRNAME, detail=True):
        # fileinfo is a dict, with file names as keys,
        # and dicts with actual file info as values;
        # we need path ({"name": "..."})
        # and URL component ({"href": "remote.php/dav/..."})
        for f in fileinfo.values():
            name = f["name"]
            href = f["href"]

            # reported path is relative to root of fs object,
            # what we need is relative to the directory that we walk
            relpath = PurePosixPath(name).relative_to(DIRNAME)

            writer.writerow([relpath, href])
