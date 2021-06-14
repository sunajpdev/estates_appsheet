#!/bin/bash
cd `dirname $0`
git fetch
git reset --hard origin/master
git merge origin/master
