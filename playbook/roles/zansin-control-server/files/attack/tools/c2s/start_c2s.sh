#!/bin/bash
# for debug
#sudo carton exec perl ./tools/c2s/c2dns.pl &
sudo carton exec perl ./tools/c2s/c2dns.pl > /dev/null 2>&1 &
