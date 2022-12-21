#!/usr/bin/env bash
# Copyright (c) 2022 José Manuel Barroso Galindo <theypsilon@gmail.com>

set -euo pipefail

git fetch origin main
git checkout --orphan main
git add .
git commit -m "-"

if git diff --quiet main origin/main ; then
    echo "No changes detected."
    exit 0
fi

git push --force origin main
