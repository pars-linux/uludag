#!/bin/bash

find ./ -iname "*.pyc" |xargs rm -rfv
find ./ -iname "*~" |xargs rm -rfv
find ./po -iname "*.mo" | xargs rm -rfv
