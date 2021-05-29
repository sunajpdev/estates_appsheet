#!/bin/bash
echo "estate cron start"
cd ~/estates_appsheet
python3 run.py > cron.log
echo "estate cron end"
exit 0
