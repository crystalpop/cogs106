#!/bin/bash

git add .
git commit -m "Update"
git push

date >> version

git add .
git commit -m "New version"
git push

