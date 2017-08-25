#!/bin/BASH_SOURCE

SOURCE="${BASH_SOURCE[0]}"
DIR="$( cd -P "$( dirname "$SOURCE")" && pwd )"

SCRIPT_DIR=$DIR/scripts

python3 $SCRIPT_DIR/release.py "($DIR)"
