#!/usr/bin/sh
pkill python3
pkill python3
pkill chromiu
sleep 5
d=$(date +%Y-%m-%d-%H-%M-%S)
cd /home/olegsvs/yepcock-size-bot
mkdir users
mkdir logs
mkdir roulette
rm wordle.png
rm wordle_screenshot_imgur_link.txt
rm wordle_not_solved_screenshot_imgur_link.txt
mkdir -p ../bot_backup/users_backups_$d/
mkdir -p ../bot_backup/logs_$d/
mv users/* ../bot_backup/users_backups_$d/
mv logs/* ../bot_backup/logs_$d/
nohup python3 get_members.py > logs/nohup_get_members_cold.log &
sleep 5
nohup python3 bot.py > logs/nohup_cold.log &
nohup python3 wordle.py > logs/nohup_wordle_cold.log &
nohup python3 stream_checker.py > logs/nohup_stream_checker.log &
