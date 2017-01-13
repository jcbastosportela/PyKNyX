#!/bin/sh

epydoc -o /tmp/PyKNyX -u http://www.github.com/M-o-a-T/pyknyx -n PyKNyX -v \
       --no-imports --show-frames --graph all --introspect-only \
       pyknyx/common pyknyx/core pyknyx/plugins pyknyx/services pyknyx/stack pyknyx/tools

