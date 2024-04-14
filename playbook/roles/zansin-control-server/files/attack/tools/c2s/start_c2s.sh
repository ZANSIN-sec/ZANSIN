#!/bin/bash
# for debug
#cd attack && sudo carton exec perl -Itools/c2s ./tools/c2s/c2dns.pl $1
#cd attack && sudo carton exec perl -Itools/c2s ./tools/c2s/c2dns.pl $1 &

cd attack && sudo carton exec perl -Itools/c2s ./tools/c2s/c2dns.pl $1 > /dev/null 2>&1 &
reset
