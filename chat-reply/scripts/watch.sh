#!/bin/bash
# Background watcher for the Chat 回复 session: exits (waking the session) as soon as the queue has status=new items.
cd "$(dirname "$0")"
while true; do
  n=$(/opt/homebrew/bin/python3 queue.py count new 2>/dev/null || echo 0)
  if [ "${n:-0}" -gt 0 ]; then echo "NEW=$n"; exit 0; fi
  sleep 60
done
