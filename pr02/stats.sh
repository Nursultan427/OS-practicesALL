#!/bin/bash

total=0
max_errors=-1
max_file=""

for f in data/*.log; do
    [ -f "$f" ] || continue

    count=$(grep -c "ERROR" "$f" || true)

    echo "$f: $count ошибок"

    total=$((total + count))

    if [ "$count" -gt "$max_errors" ]; then
        max_errors=$count
        max_file=$f
    fi
done

echo "Всего ошибок: $total"

if [ -n "$max_file" ]; then
    echo "Больше всего ошибок: $max_file ($max_errors)"
fi
