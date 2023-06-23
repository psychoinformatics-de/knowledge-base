#!/bin/bash
#
# Michael Hanke 2020

set -e -u

echo "Processing $1"

cd $1
ds_path="$(readlink -f .)"

test -f config || ( echo "not a repository: $1" && exit 1 )

rm -f info/exclude
rm -f hooks/*
test -d info && rmdir --ignore-fail-on-non-empty info
test -d hooks && rmdir --ignore-fail-on-non-empty hooks
rm -rf annex/journal
rm -f annex/index
rm -f annex/index.lck
rm -f annex/journal.lck
rm -f annex/othertmp.lck
test -d annex/othertmp && rmdir annex/othertmp
test -d ora-remote-*/transfer && rmdir --ignore-fail-on-non-empty ora-remote-*/transfer
test -d ora-remote-* && rmdir --ignore-fail-on-non-empty ora-remote-*

# uncompressed archive by default
sevenzopts=${HP_ZIPOPTS:--mx0}

objpath="$(readlink -f annex/objects)"
archivepath="$(readlink -f archives)"

if [ ! -d "$objpath" ]; then
        >&2 echo "No annex objects. Done."
        exit 0
fi

if [ ! -d "$archivepath" ]; then
        mkdir -p "$archivepath"
        # only chown when freshly created to not destroy potential
        # custom permission setup
        # whoever owns the object store, owns the archives
        chown -R --reference "$objpath" "$archivepath"
fi

mv "$objpath" "$objpath"_
objpath="$objpath"_

cd "$objpath"
# always update, also works from scratch
7z u "$archivepath/archive.7z" . $sevenzopts
chown -R --reference "$objpath" "$archivepath"/archive.7z
cd -

rm -rf "$objpath"
rmdir --ignore-fail-on-non-empty "$ds_path/annex"
