#!bin/bash
cat logs/"$(ls logs/ -1rt | grep -v stream | tail -n1)"
