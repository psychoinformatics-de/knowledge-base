import csv
from pathlib import PurePosixPath

from webdav4.fsspec import WebdavFileSystem
from datalad.api import credentials

cred = credentials(
    "get",
    name="webdav-mycred",
    return_type="item-or-list",
)
fs = WebdavFileSystem(
    "https://example.com/nextcloud/remote.php/dav/files/USERNAME/",
    auth=(cred["cred_user"], cred["cred_secret"]),
)

with open("listing.txt", "wt") as urlfile:
    writer = csv.writer(urlfile, delimiter="\t")
    writer.writerow(["name", "href"])

    for dirpath, dirinfo, fileinfo in fs.walk("test-sharing/example2", detail=True):
        # fileinfo is a dict, with file names as keys,
        # and dicts with actual file info as values;
        # we need path ({"name": "..."})
        # and URL compnent ({"href": "remote.php/dav/..."})
        for f in fileinfo.values():
            name = f["name"]
            href = f["href"]

            # reported path is relative to root of fs object,
            # what we need is relative to the directory that we walk
            relpath = PurePosixPath(name).relative_to("test-sharing/example2")

            writer.writerow((relpath, href))

# uncurl pattern - may need to adjust slashes a little
# "(?P<site>https://[^/]+)/(?P<accesspath>remote\.php/dav/files/[^/]+|public\.php/webdav)/(?P<dirpath>test-sharing/example2/)(?P<filepath>.*)"gm
