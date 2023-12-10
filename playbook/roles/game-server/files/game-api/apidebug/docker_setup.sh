#!/bin/sh
sudo docker build -t apidebug .
sudo docker run -it -p 3000:3000 --rm --name apidebug apidebug
