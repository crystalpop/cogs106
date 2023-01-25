#!/bin/bash

git add .
git commit -m "Update"
git push

date > version

git add .
git commit -m "Added 'version' file"
git push

