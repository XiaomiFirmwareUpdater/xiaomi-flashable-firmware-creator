#!/usr/bin/env bash
unzip mi-flashable-firmware-creator.zip
for i in `ls -d */`; do mv $i/lang.ts $i/`echo $i | cut -d '/' -f1`.ts; done
lrelease */*.ts
for i in `ls -d */`; do mv $i/`echo $i | cut -d '/' -f1`.qm ../; done
