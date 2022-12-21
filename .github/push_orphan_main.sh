#!/usr/bin/env bash
# Copyright (c) 2022 José Manuel Barroso Galindo <theypsilon@gmail.com>

set -euo pipefail

git checkout -f develop -b main
echo "Running detox"
detox -v -s utf_8-only -r *
echo "Detox done"
echo "Removing colons"
IFS=$'\n'
for i in $(find . -name "*:*"); do
    echo mv "${i}" "${i/:/-}"
    mv "${i}" "${i/:/-}"
done
echo "Colons removed"

git fetch origin main
git add .
git commit -m "-"

if git diff --quiet main origin/main ; then
    echo "No changes detected."
    exit 0
fi

git push --force origin main
