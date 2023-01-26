#!/bin/bash

git pull

date >> version

git add .
git commit -m "New version"
git push

