#!/bin/bash

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1iNyz3T0-vvMNB_9oYR2RStjeI6F7kNs3' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1iNyz3T0-vvMNB_9oYR2RStjeI6F7kNs3" -O cifar-10-python.tar.gz && rm -rf /tmp/cookies.txt
tar -xzvf cifar-10-python.tar.gz