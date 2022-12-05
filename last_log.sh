#!bin/bash
cat logs/"$(ls logs/ -1rt | grep -v stream | grep -v birthday | tail -n1)"
