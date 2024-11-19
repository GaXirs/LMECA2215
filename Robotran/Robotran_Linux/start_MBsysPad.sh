#!/bin/bash

# identify the path where the shell script is saved
BASEDIR=$(dirname "$0")

# Start MBsysPad with java
$BASEDIR/jre1.8.0_152/bin/java -jar $BASEDIR/MBsysPad.jar $1
