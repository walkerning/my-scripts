#!/bin/bash

for x in `ls ./*.py`; do
    if [[ ${x} != 'setup.py' ]]; then
        filename=`basename ${x}`
        filename_withoutext="${filename%.*}"
        rm -f ~/bin/${filename_withoutext}
        ln -s $(pwd)/${x} ~/bin/${filename_withoutext}
        echo 'Soft linking ' ${x} ' to ~/bin'
    fi
done
