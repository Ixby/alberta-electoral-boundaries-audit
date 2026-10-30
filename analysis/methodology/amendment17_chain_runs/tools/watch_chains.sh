#!/usr/bin/env bash
# Emit: first progress line, every 50k-step milestone, FINISHED, ERROR, STALL (>15 min no log line), process-count changes.
cd "/c/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit/data" || exit 1
declare -A mile fin errs stall
while true; do
  now=$(date +%s)
  files=$(ls simulation_checkpoints_k*/chain*.log 2>/dev/null | grep -v '/chain220\.log$' | sed 's/\.log$//')
  for f in $files; do
    n="$(basename "$(dirname "$f")" | sed 's/simulation_checkpoints_//')/$(basename "$f")"
    l=$(tail -n 1 "$f.log" 2>/dev/null)
    d=$(echo "$l" | sed -nE 's/.*\] ([0-9]+)\/.*/\1/p')
    if [ -n "$d" ]; then
      m=$((d / 50000))
      if [ "${mile[$f]:-none}" != "$m" ]; then echo "$n: $l"; mile[$f]=$m; fi
      if [ "$d" = "252500" ] && [ -z "${fin[$f]:-}" ]; then echo "$n FINISHED: $l"; fin[$f]=1; fi
    fi
    e=$(grep -vE 'Found overlaps|warnings.warn' "$f.err" 2>/dev/null | grep -cE 'Traceback|Error|cut after')
    if [ "${e:-0}" -gt "${errs[$f]:-0}" ]; then echo "$n ERROR: $(grep -vE 'Found overlaps|warnings.warn' "$f.err" | tail -n 1)"; errs[$f]=$e; fi
    mt=$(stat -c %Y "$f.log" 2>/dev/null || echo 0)
    if [ -z "${fin[$f]:-}" ] && [ $((now - mt)) -gt 900 ] && [ "${stall[$f]:-}" != "$mt" ]; then
      echo "$n STALL: no log line for $(( (now - mt) / 60 )) min; last: $l"; stall[$f]=$mt
    fi
  done
  alive=$(powershell.exe -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object CommandLine -like '*close_seats*' | Measure-Object).Count" 2>/dev/null | tr -d '\r')
  if [ -n "$alive" ] && [ "$alive" != "${pa:-}" ]; then echo "chain procs alive: $alive (2 per chain)"; pa=$alive; fi
  sleep 60
done
